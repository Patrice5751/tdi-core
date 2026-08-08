from datetime import datetime

from tdi.graphical.candle import Candle


class MT5MarketDataError(RuntimeError):
    pass


class MT5MarketDataAdapter:
    """
    Adaptateur MT5 en lecture seule.

    Il transforme les données MetaTrader 5
    en objets métier TDI.

    Aucun ordre de trading n'est envoyé ici.
    """

    def __init__(self, mt5_client):
        self._mt5 = mt5_client

    def initialize(self) -> None:
        if not self._mt5.initialize():
            raise MT5MarketDataError(
                "Impossible d'initialiser MetaTrader 5."
            )

    def shutdown(self) -> None:
        self._mt5.shutdown()

    def get_candles(
        self,
        symbol: str,
        timeframe: str,
        count: int = 100,
    ) -> list[Candle]:
        if count <= 0:
            return []

        mt5_timeframe = self._resolve_timeframe(
            timeframe
        )

        rates = self._mt5.copy_rates_from_pos(
            symbol,
            mt5_timeframe,
            0,
            count,
        )

        if rates is None:
            raise MT5MarketDataError(
                f"Impossible de récupérer les bougies "
                f"pour {symbol} {timeframe}."
            )

        candles: list[Candle] = []

        for index, rate in enumerate(rates):
            candles.append(
                Candle(
                    index=index,
                    timestamp=datetime.fromtimestamp(
                        int(rate["time"])
                    ),
                    open=float(rate["open"]),
                    high=float(rate["high"]),
                    low=float(rate["low"]),
                    close=float(rate["close"]),
                )
            )

        return candles

    def get_current_price(
        self,
        symbol: str,
    ) -> float:
        tick = self._mt5.symbol_info_tick(symbol)

        if tick is None:
            raise MT5MarketDataError(
                f"Prix actuel indisponible pour {symbol}."
            )

        bid = float(tick.bid)
        ask = float(tick.ask)

        return (bid + ask) / 2

    def _resolve_timeframe(
        self,
        timeframe: str,
    ):
        normalized = timeframe.upper()

        attribute_name = (
            f"TIMEFRAME_{normalized}"
        )

        if not hasattr(
            self._mt5,
            attribute_name,
        ):
            raise MT5MarketDataError(
                f"Timeframe MT5 non supporté : "
                f"{timeframe}"
            )

        return getattr(
            self._mt5,
            attribute_name,
        )
    def resolve_symbol(
        self,
        symbol: str,
    ) -> str:
        if self._mt5.symbol_info(symbol) is not None:
            self._mt5.symbol_select(symbol, True)
            return symbol

        symbols = self._mt5.symbols_get()

        if symbols is None:
            raise MT5MarketDataError(
                "Impossible de récupérer la liste des symboles MT5."
            )

        requested = symbol.upper()

        candidates = [
            item.name
            for item in symbols
            if item.name.upper().startswith(requested)
        ]

        if not candidates:
            raise MT5MarketDataError(
                f"Aucun symbole MT5 correspondant à {symbol}."
            )

        resolved = candidates[0]

        if not self._mt5.symbol_select(
            resolved,
            True,
        ):
            raise MT5MarketDataError(
                f"Impossible d'activer le symbole {resolved}."
            )

        return resolved
