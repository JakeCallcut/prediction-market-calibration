#Contains reusable config elements
from datetime import timedelta
from pathlib import Path

#Paths
ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = ROOT / "data" / "raw"
PROC_DATA_PATH = ROOT / "data" / "processed"
RESULTS_PATH = ROOT / "results"

#config Vars
NUM_MARKETS = 100
HORIZONS = {
    "1h": timedelta(hours=1),
    "1d": timedelta(days=1),
    "1w": timedelta(weeks=1),
    "1m": timedelta(weeks=4),
}

#API Endpoints
KALSHI_BASE = "https://external-api.kalshi.com/trade-api/v2"
GAMMA_BASE = "https://gamma-api.polymarket.com/markets"
CLOB_BASE = "https://clob.polymarket.com/prices-history"