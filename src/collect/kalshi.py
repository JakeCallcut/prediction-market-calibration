#Kalshi API Interface
#Contains interaction functions to get kalshi markets and prices
#Run as main to fetch and print 10 markets

from data_models.kalshiMarket import KalshiMarket
from datetime import datetime, timedelta, timezone
from src import config
import requests

def _lifespan_ok(raw, min_life) -> bool:
    """Helper function to check if a kalshi market has a lifetime of `min_life`"""
    o, c = raw.get("open_time"), raw.get("close_time")
    if not o or not c:
        return False
    try:
        o = datetime.fromisoformat(o.replace("Z", "+00:00"))
        c = datetime.fromisoformat(c.replace("Z", "+00:00"))
    except ValueError:
        return False
    return (c - o) >= min_life

def get_top_kalshi_markets(n: int, n_series: int, per_series: int, min_life: timedelta = timedelta(weeks=4)) -> list[KalshiMarket]:
    """Fetch the top n kalshi markets, with a lifetime of over `min_life`"""
    # rank series by volume, high first
    sp = {"include_volume": "true", "limit": 200}
    r = requests.get(f"{config.KALSHI_BASE}/series", params=sp, timeout=10)
    r.raise_for_status()
    series = r.json().get("series", [])
    series.sort(key=lambda s: float(s.get("volume") or s.get("volume_fp") or 0),
                reverse=True)

    #walk top series, pulling their settled markets until we have n
    markets = []
    for s in series[:n_series]:
        ticker = s.get("ticker") or s.get("series_ticker")
        if not ticker:
            continue
        cursor = None
        pulled = 0
        while pulled < per_series and len(markets) < n:
            params = {"series_ticker": ticker, "status": "settled",
                      "mve_filter": "exclude", "limit": 1000}
            if cursor:
                params["cursor"] = cursor
            mr = requests.get(f"{config.KALSHI_BASE}/markets", params=params, timeout=10)
            mr.raise_for_status()
            data = mr.json()
            batch = data.get("markets", [])
            if not batch:
                break
            markets.extend(KalshiMarket(raw) for raw in batch if _lifespan_ok(raw, min_life))
            pulled += len(batch)
            cursor = data.get("cursor")
            if not cursor:
                break
        if len(markets) >= n:
            break
    return markets[:n]

def _price(candle) -> float | None:
    """Helper function to extract a price from a candle, falling back to average of bid and ask price if no trades"""
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
    url = f"{config.KALSHI_BASE}/series/{series}/markets/{ticker}/candlesticks"
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
    return _price(c)

def get_kalshi_horizon_prices(market, resolved_dt):
    """Return a list of kalshi market prices for each time horizon in config"""
    if isinstance(resolved_dt, str):
        resolved_dt = datetime.fromisoformat(resolved_dt.replace("Z", "+00:00"))
    earliest = resolved_dt - max(config.HORIZONS.values())
    candles = fetch_candles(
        market.series, market.ticker,
        int(earliest.timestamp()),
        int(resolved_dt.timestamp()),      # <- the missing end_ts
        period_interval=60,
    )
    return {name: price_at(candles, resolved_dt - delta)
            for name, delta in config.HORIZONS.items()}

if __name__ == "__main__":
    markets = get_top_kalshi_markets(10, 2, 5)
    for m in markets:
        print(m)
        #print(m.title, "->", m.result, "resolved at:", m.closedTime)
