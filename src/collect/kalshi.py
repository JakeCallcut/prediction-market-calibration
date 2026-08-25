from data_models.kalshiMarket import KalshiMarket
import requests

KALSHI_BASE = "https://external-api.kalshi.com/trade-api/v2"

def fetch_kalshi_markets(n: int) -> list[KalshiMarket]:
    markets, cursor = [], None
    while len(markets) < n:
        params = {"limit": 1000, "status": "settled", "mve_filter": "exclude"}
        if cursor:
            params["cursor"] = cursor
        r = requests.get(f"{KALSHI_BASE}/markets", params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        batch = data.get("markets", [])
        if not batch:
            break
        markets.extend(KalshiMarket(raw) for raw in batch)
        cursor = data.get("cursor")
        if not cursor:
            break
    return markets[:n]

if __name__ == "__main__":
    markets = fetch_kalshi_markets(1000)
    for m in markets:
        print(f"{m.title} -> {m.result} at {m.closedTime}")