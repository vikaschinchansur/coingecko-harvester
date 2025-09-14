import os, time, requests, datetime as dt
from dotenv import load_dotenv

load_dotenv()

CG_KEY = os.getenv("CG_KEY")
PBI_URL = os.getenv("PBI_PUSH_URL")

# Check if environment variables are loaded
if not CG_KEY:
    raise ValueError("CG_KEY environment variable is not set")
if not PBI_URL:
    raise ValueError("PBI_PUSH_URL environment variable is not set")


def fetch_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "vs_currencies": "usd,aud",
        "symbols": "btc,eth",
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "include_24hr_change": "true",
        "include_last_updated_at": "true",
        "precision": "5"
    }
    headers = {"x_cg_demo_api_key": CG_KEY}
    r = requests.get(url, params=params, headers=headers, timeout=10)
    r.raise_for_status()
    return r.json()


def format_rows(payload):
    now = dt.datetime.now(dt.UTC).isoformat().replace('+00:00', 'Z')
    ingested_at = now
    rows = []
    for asset in ["btc", "eth"]:
        asset_data = payload[asset]
        row = {
            "asset": asset.upper(),
            "price_aud": asset_data["aud"],
            "timestamp": now,
            "price_usd": asset_data["usd"],
            "exchange": "coingecko",
            "source": "coingecko_api",
            "volume_24h": asset_data["usd_24h_vol"],
            "change_pct_24h": asset_data["usd_24h_change"],
            "market_cap_usd": asset_data["usd_market_cap"],
            "ingested_at": ingested_at
        }
        rows.append(row)
    return rows


def push_to_powerbi(rows):
    # Power BI expects an array of row-objects for streaming datasets
    r = requests.post(PBI_URL, json=rows, timeout=10)
    r.raise_for_status()


if __name__ == "__main__":
    while True:
        data = fetch_prices()
        rows = format_rows(data)
        push_to_powerbi(rows)
        time.sleep(60)
