#Polymarket's CLOB API interface
#Contains functions to get historical prices for a market given its CLOB ID
#to be used in conjuction with the Gamma interface

import requests
from datetime import datetime, timedelta
from src import config

def get_horizon_times(resolved_dt: datetime):
    resolved_dt = datetime.fromisoformat(resolved_dt)
    return {name: resolved_dt - delta for name, delta in config.HORIZONS.items()}

def get_price(token_id, target_dt, fidelity=720):
    r = requests.get(config.CLOB_BASE,
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

def get_clob_horizon_prices(id: str, resolved_dt: datetime):
    times = get_horizon_times(resolved_dt)
    return {name: get_price(id, dt) for name, dt in times.items()}

if __name__ == "__main__":
    pass