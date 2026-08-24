from collect.clob import get_horizon_prices
from collect.gamma import FetchGammaMarkets

def main():
    gammas = FetchGammaMarkets(2000)
    for m in gammas:
        horizon_prices = get_horizon_prices(m.clobIds[0], m.closedTime)
        print(f"{m.question}: {horizon_prices}")

if __name__ == "__main__":
    main()