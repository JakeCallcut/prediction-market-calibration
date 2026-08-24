import requests
from datetime import datetime, timezone

CLOB_BASE = "https://clob.polymarket.com/prices-history"

def price_at(token_id, target_dt, fidelity=720):
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
    return pt["p"], datetime.fromtimestamp(pt["t"], tz=timezone.utc)


if __name__ == "__main__":
    target = datetime(2026, 8, 20, tzinfo=timezone.utc)
    print(price_at(token_id="17673566063898626336042894481556069170955440532229497731331809372288232441484", target_dt=target))

