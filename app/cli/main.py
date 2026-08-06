def read_float(prompt: str) -> float:
    while True:
        value = input(prompt).strip().replace(",", ".")

        try:
            return float(value)
        except ValueError:
            print("Invalid number. Please try again.")


def main():
    print("=" * 50)
    print("Trading Decision Intelligence")
    print("Version 0.9.0")
    print("=" * 50)
    print()

    symbol = input("Symbol      : ").strip().upper()
    direction = input("Direction   : ").strip().upper()

    entry = read_float("Entry       : ")
    stop_loss = read_float("Stop Loss   : ")
    take_profit = read_float("Take Profit : ")

    print()
    print("-" * 50)
    print("TRADE SUMMARY")
    print("-" * 50)
    print(f"Symbol      : {symbol}")
    print(f"Direction   : {direction}")
    print(f"Entry       : {entry}")
    print(f"Stop Loss   : {stop_loss}")
    print(f"Take Profit : {take_profit}")
    print()
    print("Status      : Ready for analysis")


if __name__ == "__main__":
    main()

def read_float_with_default(
    prompt: str,
    default: float,
) -> float:
    while True:
        raw_value = input(f"{prompt} [{default}] : ").strip()

        if not raw_value:
            return default

        raw_value = raw_value.replace(",", ".")

        try:
            return float(raw_value)
        except ValueError:
            print("Invalid number. Please try again.")

    DEFAULT_CAPITAL = 5000.0
    DEFAULT_RISK = 1.5

    capital = read_float_with_default(
        "Capital ($)",
        DEFAULT_CAPITAL,
    )

    risk_percent = read_float_with_default(
        "Risk (%)",
        DEFAULT_RISK,
    )