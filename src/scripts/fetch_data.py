from collect.clob import get_horizon_prices
from collect.gamma import get_gamma_markets

def main():
    gammas = get_gamma_markets(2000)
    for m in gammas:
        horizon_prices = get_horizon_prices(m.clobIds[0], m.closedTime)
        print(f"{m.question} -> {m.winning_outcome}: {horizon_prices}")

if __name__ == "__main__":
    main()