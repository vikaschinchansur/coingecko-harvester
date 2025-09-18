"""CoinGecko Crypto Price Harvester - Main Application"""

import time
from dotenv import load_dotenv

from api import CoinGeckoClient
from db import MySQLClient
from streaming import PowerBIClient
from config import AppSettings



def main():
    """Main application entry point"""
    # Load environment variables
    load_dotenv()
    
    # Load and validate settings
    settings = AppSettings.from_env()
    settings.validate()
    
    # Initialize clients
    coingecko = CoinGeckoClient()
    mysql = MySQLClient()
    powerbi = PowerBIClient()
    
    print("Starting CoinGecko harvester with MySQL storage...")
    print("Fetching all data every 60 seconds...")
    
    # Wait for MySQL to be ready (useful when starting with docker-compose)
    time.sleep(settings.startup_delay_seconds)
    
    # Main loop - fetch everything every 60 seconds
    while True:
        try:
            print("\n--- Fetching all data ---")
            
            # 1. Fetch and process crypto prices
            print("Fetching crypto prices...")
            data = coingecko.fetch_prices()
            mysql.save_crypto_prices(data)
            rows = powerbi.format_rows(data)
            success, response_code, error_msg = powerbi.push_data(rows)
            mysql.save_powerbi_log(rows, success, response_code, error_msg)
            
            # 2. Fetch supported currencies
            try:
                print("Fetching supported currencies...")
                currencies = coingecko.get_supported_currencies()
                mysql.save_supported_currencies(currencies)
            except Exception as e:
                print(f"Error fetching supported currencies: {e}")
            
            # 3. Fetch BTC exchange rates
            try:
                print("Fetching BTC exchange rates...")
                exchange_rates = coingecko.get_exchange_rates()
                mysql.save_btc_exchange_rates(exchange_rates)
                exchange_rows = powerbi.format_exchange_rates(exchange_rates)
                if exchange_rows:
                    success, response_code, error_msg = powerbi.push_data(exchange_rows, "exchange_rates")
                    mysql.save_powerbi_log(exchange_rows, success, response_code, error_msg)
            except Exception as e:
                print(f"Error fetching exchange rates: {e}")
            
            # 4. Fetch Bitcoin companies holdings
            try:
                print("Fetching Bitcoin company holdings...")
                companies_data = coingecko.get_bitcoin_companies()
                mysql.save_bitcoin_companies(companies_data)
                company_rows = powerbi.format_bitcoin_companies(companies_data)
                if company_rows:
                    success, response_code, error_msg = powerbi.push_data(company_rows, "companies")
                    mysql.save_powerbi_log(company_rows, success, response_code, error_msg)
            except Exception as e:
                print(f"Error fetching Bitcoin companies: {e}")
            
            print("All data fetched successfully. Waiting 60 seconds...")
            
            # Wait 60 seconds before next fetch
            time.sleep(60)
            
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(60)


if __name__ == "__main__":
    main()