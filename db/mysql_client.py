"""MySQL database client for crypto price storage"""

import json
import os
from typing import Optional, Dict, Any, List
import mysql.connector
from mysql.connector import Error
from datetime import datetime


class MySQLClient:
    """Handles MySQL database operations for crypto price data"""
    
    def __init__(self):
        """Initialize MySQL client with configuration from environment variables"""
        self.config = {
            'host': os.getenv("MYSQL_HOST"),
            'port': os.getenv("MYSQL_PORT"),
            'database': os.getenv("MYSQL_DATABASE"),
            'user': os.getenv("MYSQL_USER"),
            'password': os.getenv("MYSQL_PASSWORD")
        }
    
    def _get_connection(self) -> Optional[mysql.connector.MySQLConnection]:
        """
        Create and return a MySQL database connection
        
        Returns:
            MySQLConnection object or None if connection fails
        """
        try:
            # Check if all required config is present
            if not all(self.config.values()):
                print("MySQL configuration incomplete. Skipping database operations.")
                return None
            
            connection = mysql.connector.connect(**self.config)
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def save_crypto_prices(self, data: Dict[str, Any]) -> bool:
        """
        Save cryptocurrency price data to database
        
        Args:
            data: Dictionary of crypto price data from API
            
        Returns:
            True if save successful, False otherwise
        """
        connection = self._get_connection()
        if not connection:
            print("Failed to connect to database, skipping save")
            return False
        
        try:
            cursor = connection.cursor()
            
            insert_query = """
                INSERT INTO crypto_prices 
                (coin_id, coin_name, price_usd, price_usd_24h_change, 
                 market_cap_usd, volume_24h_usd, last_updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            # Prepare data for insertion
            for coin_id, coin_data in data.items():
                # Convert Unix timestamp to datetime
                import time
                last_updated = datetime.fromtimestamp(
                    coin_data.get('last_updated_at', time.time())
                )
                
                values = (
                    coin_id,
                    coin_id.upper(),
                    coin_data.get('usd', 0),
                    coin_data.get('usd_24h_change', 0),
                    coin_data.get('usd_market_cap', 0),
                    coin_data.get('usd_24h_vol', 0),
                    last_updated
                )
                
                cursor.execute(insert_query, values)
            
            connection.commit()
            print(f"Saved {len(data)} crypto prices to database")
            return True
            
        except Error as e:
            print(f"Error saving to MySQL: {e}")
            connection.rollback()
            return False
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def save_supported_currencies(self, currencies: List[str]) -> bool:
        """
        Save supported currencies list to database
        
        Args:
            currencies: List of currency codes
            
        Returns:
            True if save successful, False otherwise
        """
        connection = self._get_connection()
        if not connection:
            print("Failed to connect to database, skipping save")
            return False
        
        try:
            cursor = connection.cursor()
            
            # Insert or update currencies
            insert_query = """
                INSERT INTO supported_currencies (currency_code, is_crypto)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE updated_at = CURRENT_TIMESTAMP
            """
            
            for currency in currencies:
                # Simple heuristic: currencies with 3 letters are usually fiat
                is_crypto = len(currency) > 3 or currency in ['btc', 'eth', 'bnb', 'ada', 'dot']
                cursor.execute(insert_query, (currency, is_crypto))
            
            connection.commit()
            print(f"Saved {len(currencies)} supported currencies to database")
            return True
            
        except Error as e:
            print(f"Error saving supported currencies: {e}")
            connection.rollback()
            return False
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def save_btc_exchange_rates(self, rates_data: Dict[str, Any]) -> bool:
        """
        Save BTC exchange rates to database
        
        Args:
            rates_data: Dictionary with exchange rates data
            
        Returns:
            True if save successful, False otherwise
        """
        connection = self._get_connection()
        if not connection:
            print("Failed to connect to database, skipping save")
            return False
        
        try:
            cursor = connection.cursor()
            
            insert_query = """
                INSERT INTO btc_exchange_rates 
                (currency_code, currency_name, currency_type, rate_value, unit)
                VALUES (%s, %s, %s, %s, %s)
            """
            
            rates = rates_data.get('rates', {})
            
            for currency_code, rate_info in rates.items():
                currency_type = rate_info.get('type', 'unknown')
                values = (
                    currency_code,
                    rate_info.get('name', currency_code),
                    currency_type,
                    rate_info.get('value', 0),
                    rate_info.get('unit', currency_code)
                )
                cursor.execute(insert_query, values)
            
            connection.commit()
            print(f"Saved {len(rates)} BTC exchange rates to database")
            return True
            
        except Error as e:
            print(f"Error saving BTC exchange rates: {e}")
            connection.rollback()
            return False
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def save_bitcoin_companies(self, companies_data: Dict[str, Any]) -> bool:
        """
        Save Bitcoin company holdings data to database
        
        Args:
            companies_data: Dictionary with company holdings data
            
        Returns:
            True if save successful, False otherwise
        """
        connection = self._get_connection()
        if not connection:
            print("Failed to connect to database, skipping save")
            return False
        
        try:
            cursor = connection.cursor()
            
            # Save individual companies
            company_insert_query = """
                INSERT INTO bitcoin_companies 
                (company_name, symbol, country, total_holdings, 
                 total_entry_value_usd, total_current_value_usd, 
                 percentage_of_total_supply, data_source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            companies = companies_data.get('companies', [])
            
            for company in companies:
                values = (
                    company.get('name', ''),
                    company.get('symbol', None),
                    company.get('country', None),
                    company.get('total_holdings', 0),
                    company.get('total_entry_value_usd', None),
                    company.get('total_current_value_usd', None),
                    company.get('percentage_of_total_supply', None),
                    'public_companies'
                )
                cursor.execute(company_insert_query, values)
            
            # Save treasury summary
            summary_insert_query = """
                INSERT INTO bitcoin_treasury_summary 
                (total_holdings, total_value_usd, companies_count, 
                 market_cap_dominance, data_source)
                VALUES (%s, %s, %s, %s, %s)
            """
            
            summary_values = (
                companies_data.get('total_holdings_btc', 0),
                companies_data.get('total_value_usd', None),
                companies_data.get('companies', []).__len__(),
                companies_data.get('market_cap_dominance', None),
                'public_companies'
            )
            cursor.execute(summary_insert_query, summary_values)
            
            connection.commit()
            print(f"Saved {len(companies)} Bitcoin companies to database")
            return True
            
        except Error as e:
            print(f"Error saving Bitcoin companies: {e}")
            connection.rollback()
            return False
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def save_powerbi_log(self, rows: List[Dict], success: bool, 
                        response_code: Optional[int] = None, 
                        error_message: Optional[str] = None) -> None:
        """
        Log Power BI push attempts to database
        
        Args:
            rows: Data rows that were pushed
            success: Whether the push was successful
            response_code: HTTP response code
            error_message: Error message if failed
        """
        connection = self._get_connection()
        if not connection:
            return
        
        try:
            cursor = connection.cursor()
            
            insert_query = """
                INSERT INTO powerbi_push_logs 
                (status, response_code, error_message, data_pushed)
                VALUES (%s, %s, %s, %s)
            """
            
            status = "success" if success else "failure"
            data_json = json.dumps(rows[:2])  # Save sample of data
            
            cursor.execute(insert_query, (status, response_code, error_message, data_json))
            connection.commit()
            
        except Error as e:
            print(f"Error logging to MySQL: {e}")
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()