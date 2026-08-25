import requests
from datetime import datetime, timezone, timedelta

CLOB_BASE = "https://clob.polymarket.com/prices-history"
HORIZONS = {
    "1h": timedelta(hours=1),
    "1d": timedelta(days=1),
    "1w": timedelta(weeks=1),
    "1m": timedelta(weeks=4),
}

def get_horizon_times(resolved_dt: datetime):
    resolved_dt = datetime.fromisoformat(resolved_dt)
    return {name: resolved_dt - delta for name, delta in HORIZONS.items()}

def get_price(token_id, target_dt, fidelity=720):
    r = requests.get(CLOB_BASE,
                     params={"market": token_id, "interval": "max",
                             "fidelity": fidelity}, timeout=15)
    r.raise_for_status()
    history = sorted(r.json().get("history", []), key=lambda pt: pt["t"])
    target_ts = int(target_dt.timestamp())
    past = [pt for pt in history if pt["t"] <= target_ts]
    if not past:
        return None            # no data before that moment; drop this market
    pt = past[-1]
    return pt["p"]

def get_horizon_prices(id: str, resolved_dt: datetime):
    times = get_horizon_times(resolved_dt)
    return {name: get_price(id, dt) for name, dt in times.items()}