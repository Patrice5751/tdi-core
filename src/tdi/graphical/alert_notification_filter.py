class AlertNotificationFilter:
    def __init__(self):
        self._last_by_symbol: dict[
            str,
            tuple[str, str],
        ] = {}

        self._previous_warning_by_symbol: dict[
            str,
            tuple[str, str],
        ] = {}

    def should_notify(
        self,
        symbol: str,
        level: str,
        message: str,
    ) -> bool:
        normalized_level = level.upper()
        signature = (
            normalized_level,
            message,
        )

        if normalized_level == "HIGH":
            self._last_by_symbol[symbol] = signature
            return True

        if normalized_level == "WARNING":
            previous_warning = (
                self._previous_warning_by_symbol.get(symbol)
            )

            if previous_warning == signature:
                return False

            self._previous_warning_by_symbol[symbol] = (
                signature
            )

        self._last_by_symbol[symbol] = signature
        return True