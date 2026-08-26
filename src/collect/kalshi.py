from data_models.kalshiMarket import KalshiMarket
from datetime import datetime, timedelta, timezone
import requests


KALSHI_BASE = "https://external-api.kalshi.com/trade-api/v2"

HORIZONS = {
    "1h": timedelta(hours=1),
    "1d": timedelta(days=1),
    "1w": timedelta(weeks=1),
    "1m": timedelta(weeks=4),
}

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

def _price(candle):
    p = candle.get("price", {})
    v = p.get("close_dollars")
    if v is not None:
        return float(v)
    # no trade in this interval: fall back to the bid/ask midpoint
    bid = candle.get("yes_bid", {}).get("close_dollars")
    ask = candle.get("yes_ask", {}).get("close_dollars")
    if bid is not None and ask is not None:
        return (float(bid) + float(ask)) / 2
    return float(bid) if bid is not None else (float(ask) if ask is not None else None)

def fetch_candles(series, ticker, start_ts, end_ts, period_interval=60):
    url = f"{KALSHI_BASE}/series/{series}/markets/{ticker}/candlesticks"
    r = requests.get(url, params={
        "start_ts": start_ts, "end_ts": end_ts,
        "period_interval": period_interval,
        "include_latest_before_start": "true",
    }, timeout=15)
    r.raise_for_status()
    return sorted(r.json().get("candlesticks", []), key=lambda c: c["end_period_ts"])

def price_at(candles, target_dt):
    target_ts = int(target_dt.timestamp())
    past = [c for c in candles if c["end_period_ts"] <= target_ts and _price(c) is not None]
    if not past:
        return None
    c = past[-1]
    return _price(c), datetime.fromtimestamp(c["end_period_ts"], tz=timezone.utc)

def get_kalshi_horizon_prices(market, resolved_dt):
    resolved_dt = datetime.fromisoformat(resolved_dt)
    earliest = resolved_dt - max(HORIZONS.values())
    candles = fetch_candles(
        market.series, market.ticker,
        int(earliest.timestamp())
    )
    return {name: price_at(candles, resolved_dt - delta)
            for name, delta in HORIZONS.items()}

if __name__ == "__main__":
    pass
    # markets = fetch_kalshi_markets(10)
    # m = markets[0]
    # resolved = datetime.fromisoformat(m.closedTime) if isinstance(m.closedTime, str) else m.closedTime
    # start = int((resolved - timedelta(days=30)).timestamp())
    # end = int(resolved.timestamp())
    #
    # url = f"{KALSHI_BASE}/series/{m.series}/markets/{m.ticker}/candlesticks"
    # print("series:", m.series, "ticker:", m.ticker)
    # print("url:", url)
    # r = requests.get(url, params={"start_ts": start, "end_ts": end,
    #                               "period_interval": 60,
    #                               "include_latest_before_start": "true"}, timeout=15)
    # print("status:", r.status_code)
    # print("body:", r.text[:400])