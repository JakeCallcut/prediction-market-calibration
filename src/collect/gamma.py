import requests
from data_models.gammaMarket import GammaMarket

GAMMA_BASE = "https://gamma-api.polymarket.com/markets"

def FetchMarkets(n: int) -> list[GammaMarket]:
    markets = []
    offset = 0
    while len(markets) < n:
        r = requests.get(GAMMA_BASE, params={
            "limit": 100,
            "offset": offset,
            "closed": "true",
            "order": "endDate",
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
    markets = FetchMarkets(1000)
    for m in markets:
        print(m.question, m.outcomes, "->", m.winning_outcome, "resolved", m.resolved, "at", m.closedTime)