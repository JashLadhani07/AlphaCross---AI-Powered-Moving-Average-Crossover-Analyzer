import requests
import pandas as pd
import io
from functools import lru_cache
from pathlib import Path

NSE_500_URL = "https://www.niftyindices.com/IndexConstituent/ind_nifty500list.csv"

# Local backup CSV
BASE_DIR = Path(__file__).resolve().parent.parent
LOCAL_CSV = BASE_DIR / "data" / "nifty500.csv"

# Last-resort fallback
FALLBACK = [
    {"Symbol": "RELIANCE", "Industry": "Energy"},
    {"Symbol": "TCS", "Industry": "IT"},
    {"Symbol": "INFY", "Industry": "IT"},
    {"Symbol": "HDFCBANK", "Industry": "Banking"},
]


@lru_cache(maxsize=1)
def fetch_nse500_symbols():
    """
    Priority:
    1. Download latest official Nifty 500 list
    2. If download fails, use local CSV
    3. If local CSV also fails, use minimal fallback
    """

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # ==========================
    # Try official Nifty website
    # ==========================
    try:
        print("Fetching latest NSE 500 list from Nifty...")

        response = requests.get(
            NSE_500_URL,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        df = pd.read_csv(io.StringIO(response.text))

        if "Symbol" not in df.columns:
            raise ValueError("Invalid CSV downloaded")

        print(f"Loaded {len(df)} stocks from Nifty website.")

        return df[["Symbol", "Industry"]].to_dict("records")

    except Exception as e:
        print(f"Online fetch failed: {e}")

    # ==========================
    # Local CSV Backup
    # ==========================
    try:
        print("Loading local backup CSV...")

        df = pd.read_csv(LOCAL_CSV)

        if "Symbol" not in df.columns:
            raise ValueError("Invalid local CSV")

        print(f"Loaded {len(df)} stocks from local CSV.")

        return df[["Symbol", "Industry"]].to_dict("records")

    except Exception as e:
        print(f"Local CSV failed: {e}")

    # ==========================
    # Final fallback
    # ==========================
    print("Using minimal fallback (4 stocks).")

    return FALLBACK


def get_nse500_status():
    stocks = fetch_nse500_symbols()

    return {
        "source": "dynamic with local backup",
        "count": len(stocks),
        "sample": stocks[:5]
    }