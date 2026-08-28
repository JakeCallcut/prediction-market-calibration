from collect.clob import get_clob_horizon_prices
from collect.gamma import get_top_gamma_markets
from collect.kalshi import get_top_kalshi_markets, get_kalshi_horizon_prices
import pandas as pd
from pathlib import Path

def fetch_data(num_markets:int = 100):

    k_nseries = 10
    k_nmarkets = num_markets // k_nseries
    entries = []

    print("🔹Fetching Polymarket markets...\n")
    gammas = get_top_gamma_markets(num_markets)
    print("❇️Fetching Kalshi markets...\n")
    kalshis = get_top_kalshi_markets(num_markets, k_nseries, k_nmarkets)

    print("🔹Resolving Polymarket horizons...\n")
    for m in gammas:
        y = 1 if m.winning_outcome == "Yes" else 0 if m.winning_outcome == "No" else None
        if y is None:
            continue
        prices = get_clob_horizon_prices(m.clobIds[0], m.closedTime)
        for horizon, price in prices.items():
            if price is None:
                continue
            entries.append({"source": "polymarket", "question": m.question, "horizon": horizon, "forecast": price, "outcome": y})
        print(f"🔹Resolved Market: {m.question}: {m.winning_outcome}")

    print("❇️Resolving Kalshi horizons...\n")
    for m in kalshis:
        y = m.result
        if y is None:
            continue
        prices = get_kalshi_horizon_prices(m, m.closedTime)
        for horizon, price in prices.items():
            if price is None:
                continue
            entries.append({"source": "kalshi", "question": m.title,
                         "horizon": horizon, "forecast": price, "outcome": y})
        print(f"❇️Resolved Market: {m.title}: {m.result}")

    df = pd.DataFrame(entries)
    return df

if __name__ == "__main__":
    DATA_PATH = Path("../../data/raw/")
    df = fetch_data(500)
    df.to_csv(DATA_PATH / "market_data.csv", index=False)