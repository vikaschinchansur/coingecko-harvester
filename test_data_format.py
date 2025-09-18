#!/usr/bin/env python3
"""Test script to verify data format for Power BI"""

from dotenv import load_dotenv
from api import CoinGeckoClient
from streaming import PowerBIClient
import json

# Load environment variables
load_dotenv()

# Initialize clients
coingecko = CoinGeckoClient()
powerbi = PowerBIClient()

print("Fetching crypto prices from CoinGecko...")
data = coingecko.fetch_prices()
print("\nRaw data from CoinGecko:")
print(json.dumps(data, indent=2))

print("\n" + "="*50)
print("Formatting data for Power BI...")
rows = powerbi.format_rows(data)
print("\nFormatted data for Power BI:")
for row in rows:
    print(json.dumps(row, indent=2))
    print("-" * 30)

print("\n" + "="*50)
print("\nKey observations:")
for row in rows:
    asset = row.get('asset', 'Unknown')
    price_usd = row.get('price_usd', 0)
    print(f"{asset}: ${price_usd:,.2f} USD")