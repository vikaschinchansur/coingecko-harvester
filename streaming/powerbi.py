"""Power BI streaming dataset client"""

import os
import requests
from datetime import datetime, timezone
from typing import Dict, Any, List


class PowerBIClient:
    """Handles Power BI streaming dataset operations"""
    
    def __init__(self):
        """Initialize Power BI client with push URLs from environment"""
        self.prices_url = os.getenv("PBI_PRICES_PUSH_URL")
        self.exchange_rates_url = os.getenv("PBI_EXCHANGE_RATES_URL")
        self.companies_url = os.getenv("PBI_COMPANIES_URL")
        
        if not self.prices_url:
            raise ValueError("PBI_PRICES_PUSH_URL environment variable is not set")
    
    def format_rows(self, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Format crypto price data for Power BI streaming dataset
        
        Args:
            payload: Raw data from CoinGecko API
            
        Returns:
            List of formatted rows for Power BI
        """
        now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        rows = []
        
        for asset_id, asset_data in payload.items():
            row = {
                "asset": asset_id.upper(),
                "price_aud": asset_data.get("aud", 0),
                "timestamp": now,
                "price_usd": asset_data.get("usd", 0),
                "exchange": "coingecko",
                "source": "coingecko_api",
                "volume_24h": asset_data.get("usd_24h_vol", 0),
                "change_pct_24h": asset_data.get("usd_24h_change", 0),
                "market_cap_usd": asset_data.get("usd_market_cap", 0),
                "ingested_at": now
            }
            rows.append(row)
        
        return rows
    
    def format_exchange_rates(self, rates_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Format BTC exchange rates for Power BI streaming dataset
        
        Args:
            rates_data: Exchange rates data from CoinGecko API
            
        Returns:
            List of formatted rows for Power BI
        """
        now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        rows = []
        rates = rates_data.get('rates', {})
        
        # Select key currencies for Power BI
        key_currencies = ['usd', 'eur', 'gbp', 'jpy', 'aud', 'cad', 'chf', 'cny', 'inr', 'krw']
        
        for currency in key_currencies:
            if currency in rates:
                rate_info = rates[currency]
                row = {
                    "base_currency": "BTC",
                    "target_currency": currency.upper(),
                    "exchange_rate": rate_info.get('value', 0),
                    "currency_type": rate_info.get('type', 'unknown'),
                    "currency_name": rate_info.get('name', currency),
                    "timestamp": now
                }
                rows.append(row)
        
        return rows
    
    def format_bitcoin_companies(self, companies_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Format Bitcoin company holdings for Power BI streaming dataset
        
        Args:
            companies_data: Company holdings data from CoinGecko API
            
        Returns:
            List of formatted rows for Power BI
        """
        now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        rows = []
        companies = companies_data.get('companies', [])[:10]  # Top 10 companies
        
        for company in companies:
            row = {
                "company_name": company.get('name', ''),
                "ticker_symbol": company.get('symbol', ''),
                "country": company.get('country', ''),
                "total_btc": company.get('total_holdings', 0),
                "total_value_usd": company.get('total_current_value_usd', 0),
                "percent_of_supply": company.get('percentage_of_total_supply', 0),
                "timestamp": now
            }
            rows.append(row)
        
        # Add summary row
        if companies_data:
            summary_row = {
                "company_name": "TOTAL_HOLDINGS",
                "ticker_symbol": "SUMMARY",
                "country": "ALL",
                "total_btc": companies_data.get('total_holdings_btc', 0),
                "total_value_usd": companies_data.get('total_value_usd', 0),
                "percent_of_supply": companies_data.get('market_cap_dominance', 0),
                "timestamp": now
            }
            rows.append(summary_row)
        
        return rows
    
    def push_data(self, rows: List[Dict[str, Any]], dataset_type: str = "prices") -> tuple[bool, int, str]:
        """
        Push data to Power BI streaming dataset
        
        Args:
            rows: Formatted data rows to push
            dataset_type: Type of dataset ("prices", "exchange_rates", "companies")
            
        Returns:
            Tuple of (success, response_code, error_message)
        """
        # Select appropriate URL based on dataset type
        url_map = {
            "prices": self.prices_url,
            "exchange_rates": self.exchange_rates_url,
            "companies": self.companies_url
        }
        
        push_url = url_map.get(dataset_type, self.prices_url)
        
        # Skip if URL is not configured or is placeholder
        if not push_url or "paste_your" in push_url:
            print(f"Power BI {dataset_type} URL not configured, skipping push")
            return False, None, f"{dataset_type} URL not configured"
        
        try:
            response = requests.post(push_url, json=rows, timeout=10)
            response.raise_for_status()
            print(f"Successfully pushed {dataset_type} to Power BI")
            return True, response.status_code, None
            
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            response_code = None
            
            if hasattr(e, 'response') and e.response:
                response_code = e.response.status_code
            
            print(f"Failed to push {dataset_type} to Power BI: {error_msg}")
            return False, response_code, error_msg