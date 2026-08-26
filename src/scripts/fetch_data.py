from collect.clob import get_clob_horizon_prices
from collect.gamma import get_top_gamma_markets
from collect.kalshi import get_top_kalshi_markets, get_kalshi_horizon_prices
import pandas as pd

def fetch_data(num_markets:int = 5000):

    k_nseries = 10
    k_nmarkets = num_markets // k_nseries
    gamma_df = pd.DataFrame()
    kalshi_df = pd.DataFrame()

    print("🔹Fetching Polymarket markets...\n")
    gammas = get_top_gamma_markets(num_markets)
    print("❇️Fetching Kalshi markets...\n")
    kalshis = get_top_kalshi_markets(num_markets, k_nseries, k_nmarkets)

    print("🔹Calculating Polymarket horizon prices...\n")
    for m in gammas:
        g_horizon_prices = get_clob_horizon_prices(m.clobIds[0], m.closedTime)
        print(f"{m.question} -> {m.winning_outcome}: {g_horizon_prices}")

    print("\n")
    print("❇️Calculating Kalshi horizon prices...\n")
    for m in kalshis:
        k_horizon_prices = get_kalshi_horizon_prices(m, m.closedTime)
        print(f"{m.title} -> {m.result}: {k_horizon_prices}")

if __name__ == "__main__":
    fetch_data(50)