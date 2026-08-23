import requests
from data_models.gammaMarket import GammaMarket

GAMMA_BASE = "https://gamma-api.polymarket.com/markets"

r = requests.get(GAMMA_BASE,
                params={"limit": 1000, "closed": "true",
                         "order": "endDate", "ascending": "false"}, timeout=10)

markets = [GammaMarket(raw) for raw in r.json()]   # list of objects

for m in markets:
    print(m.question, m.outcomes, "->", m.winning_outcome, "resolved:", m.resolved)