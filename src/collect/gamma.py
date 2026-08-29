#Polymarket's Gamma API Interface
#Contains function to get N top markets from polymarket
#run as main to fetch and print 10 markets

from data_models.gammaMarket import GammaMarket
import requests

GAMMA_BASE = "https://gamma-api.polymarket.com/markets"

def get_top_gamma_markets(n: int) -> list[GammaMarket]:
    markets = []
    offset = 0
    while len(markets) < n:
        r = requests.get(GAMMA_BASE, params={
            "limit": 100,
            "offset": offset,
            "closed": "true",
            "order": "volumeNum",
            "ascending": "false",
        }, timeout=10)
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        markets.extend(GammaMarket(raw) for raw in batch)
        offset += 100
    return markets[:n]


if __name__ == "__main__":
    markets = get_top_gamma_markets(10)
    for m in markets:
        print(m.question, m.outcomes, "->", m.winning_outcome, m.winning_index, "resolved at", m.closedTime)