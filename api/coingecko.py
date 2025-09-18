"""CoinGecko API client for fetching cryptocurrency prices"""

import os
import requests
from typing import Dict, Any, List


class CoinGeckoClient:
    """Handles all CoinGecko API interactions"""
    
    # Default coins to track
    DEFAULT_COINS = ["btc", "eth", "xrp", "usdt", "sol", "bnb", "usdc", "doge", "ada", "avax", "shib"]
    
    def __init__(self):
        """Initialize CoinGecko client with API key from environment"""
        self.api_key = os.getenv("CG_KEY")
        if not self.api_key:
            raise ValueError("CG_KEY environment variable is not set")
        
        self.base_url = "https://api.coingecko.com/api/v3"
        self.coins = self.DEFAULT_COINS
    
    def fetch_prices(self, coins: List[str] = None) -> Dict[str, Any]:
        """
        Fetch current prices for specified cryptocurrencies
        
        Args:
            coins: List of coin symbols to fetch (uses default if None)
            
        Returns:
            Dictionary with price data for each coin
        """
        if coins:
            self.coins = coins
        
        url = f"{self.base_url}/simple/price"
        
        params = {
            "vs_currencies": "usd,aud",
            "symbols": ",".join(self.coins),
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true",
            "include_last_updated_at": "true",
            "precision": "5"
        }
        
        headers = {
            "x_cg_demo_api_key": self.api_key
        }
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching prices from CoinGecko: {e}")
            raise
    
    def get_supported_currencies(self) -> List[str]:
        """
        Fetch list of supported vs currencies
        
        Returns:
            List of supported currency codes
        """
        url = f"{self.base_url}/simple/supported_vs_currencies"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching supported currencies: {e}")
            raise
    
    def get_exchange_rates(self) -> Dict[str, Any]:
        """
        Fetch BTC exchange rates to all supported currencies
        
        Returns:
            Dictionary with BTC exchange rates
        """
        url = f"{self.base_url}/exchange_rates"
        
        headers = {
            "x_cg_demo_api_key": self.api_key
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching exchange rates: {e}")
            raise
    
    def get_bitcoin_companies(self) -> Dict[str, Any]:
        """
        Fetch public companies holding Bitcoin
        
        Returns:
            Dictionary with companies' Bitcoin holdings data
        """
        url = f"{self.base_url}/companies/public_treasury/bitcoin"
        
        headers = {
            "x_cg_demo_api_key": self.api_key
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Bitcoin companies data: {e}")
            raise