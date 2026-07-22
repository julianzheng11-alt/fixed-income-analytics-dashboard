import pandas as pd
import yfinance as yf


TREASURY_TICKERS = {
    "3M": "^IRX",
    "5Y": "^FVX",
    "10Y": "^TNX",
    "30Y": "^TYX",
}


def get_treasury_data(period="1mo"):
    treasury_data = {}

    for maturity, ticker in TREASURY_TICKERS.items():
        data = yf.download(
            ticker,
            period=period,
            progress=False,
            auto_adjust=False,
        )

        if data.empty:
            print(f"No data found for {maturity}")
            continue

        close_prices = data["Close"]


        if isinstance(close_prices, pd.DataFrame):
            close_prices = close_prices.iloc[:, 0]

        treasury_data[maturity] = close_prices

    yield_percentages = pd.DataFrame(treasury_data)

    return yield_percentages


def get_latest_yield_curve():
    yield_percentages = get_treasury_data()

    if yield_percentages.empty:
        return pd.Series(dtype=float)

    return yield_percentages.ffill().iloc[-1]


if __name__ == "__main__":
    latest_curve = get_latest_yield_curve()

    print("Latest US Treasury yields:\n")

    for maturity, value in latest_curve.items():
        print(f"{maturity}: {value:.2f}%")