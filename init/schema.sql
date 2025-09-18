-- Create database if not exists
CREATE DATABASE IF NOT EXISTS coingecko_db;
USE coingecko_db;

-- Table to store raw price data from CoinGecko API
CREATE TABLE IF NOT EXISTS crypto_prices (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    coin_id VARCHAR(50) NOT NULL,
    coin_name VARCHAR(100),
    price_usd DECIMAL(20, 8) NOT NULL,
    price_usd_24h_change DECIMAL(10, 4),
    market_cap_usd DECIMAL(25, 2),
    volume_24h_usd DECIMAL(25, 2),
    last_updated_at TIMESTAMP,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_coin_id (coin_id),
    INDEX idx_fetched_at (fetched_at),
    INDEX idx_coin_fetched (coin_id, fetched_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table to store aggregated hourly data for reporting
CREATE TABLE IF NOT EXISTS crypto_prices_hourly (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    coin_id VARCHAR(50) NOT NULL,
    hour_timestamp TIMESTAMP NOT NULL,
    avg_price_usd DECIMAL(20, 8),
    min_price_usd DECIMAL(20, 8),
    max_price_usd DECIMAL(20, 8),
    open_price_usd DECIMAL(20, 8),
    close_price_usd DECIMAL(20, 8),
    sample_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_coin_hour (coin_id, hour_timestamp),
    INDEX idx_hour_timestamp (hour_timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table to store Power BI push logs
CREATE TABLE IF NOT EXISTS powerbi_push_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    push_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('success', 'failure') NOT NULL,
    response_code INT,
    error_message TEXT,
    data_pushed JSON,
    INDEX idx_push_timestamp (push_timestamp),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table to store supported currencies
CREATE TABLE IF NOT EXISTS supported_currencies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    currency_code VARCHAR(10) UNIQUE NOT NULL,
    currency_name VARCHAR(100),
    is_crypto BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_currency_code (currency_code),
    INDEX idx_is_crypto (is_crypto)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table to store BTC exchange rates
CREATE TABLE IF NOT EXISTS btc_exchange_rates (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    currency_code VARCHAR(10) NOT NULL,
    currency_name VARCHAR(100),
    currency_type VARCHAR(20), -- 'fiat' or 'crypto'
    rate_value DECIMAL(30, 10) NOT NULL,
    unit VARCHAR(50),
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_currency_code (currency_code),
    INDEX idx_fetched_at (fetched_at),
    INDEX idx_currency_type (currency_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table to store Bitcoin public companies holdings
CREATE TABLE IF NOT EXISTS bitcoin_companies (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    symbol VARCHAR(20),
    country VARCHAR(100),
    total_holdings DECIMAL(20, 8) NOT NULL,
    total_entry_value_usd DECIMAL(25, 2),
    total_current_value_usd DECIMAL(25, 2),
    percentage_of_total_supply DECIMAL(10, 6),
    data_source VARCHAR(50), -- 'public_companies' or 'private_companies'
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_company_name (company_name),
    INDEX idx_symbol (symbol),
    INDEX idx_country (country),
    INDEX idx_fetched_at (fetched_at),
    INDEX idx_data_source (data_source)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table for aggregate Bitcoin treasury data
CREATE TABLE IF NOT EXISTS bitcoin_treasury_summary (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    total_holdings DECIMAL(25, 8) NOT NULL,
    total_value_usd DECIMAL(30, 2),
    companies_count INT,
    market_cap_dominance DECIMAL(10, 6),
    data_source VARCHAR(50), -- 'public_companies' or 'private_companies'
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_fetched_at (fetched_at),
    INDEX idx_data_source (data_source)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create a view for the latest prices
CREATE OR REPLACE VIEW latest_crypto_prices AS
SELECT 
    cp1.coin_id,
    cp1.coin_name,
    cp1.price_usd,
    cp1.price_usd_24h_change,
    cp1.market_cap_usd,
    cp1.volume_24h_usd,
    cp1.last_updated_at,
    cp1.fetched_at
FROM crypto_prices cp1
INNER JOIN (
    SELECT coin_id, MAX(fetched_at) as max_fetched_at
    FROM crypto_prices
    GROUP BY coin_id
) cp2 ON cp1.coin_id = cp2.coin_id AND cp1.fetched_at = cp2.max_fetched_at;

-- View for latest exchange rates
CREATE OR REPLACE VIEW latest_btc_exchange_rates AS
SELECT 
    ber1.currency_code,
    ber1.currency_name,
    ber1.currency_type,
    ber1.rate_value,
    ber1.unit,
    ber1.fetched_at
FROM btc_exchange_rates ber1
INNER JOIN (
    SELECT currency_code, MAX(fetched_at) as max_fetched_at
    FROM btc_exchange_rates
    GROUP BY currency_code
) ber2 ON ber1.currency_code = ber2.currency_code AND ber1.fetched_at = ber2.max_fetched_at;

-- View for latest company holdings
CREATE OR REPLACE VIEW latest_bitcoin_companies AS
SELECT 
    bc1.*
FROM bitcoin_companies bc1
INNER JOIN (
    SELECT company_name, MAX(fetched_at) as max_fetched_at
    FROM bitcoin_companies
    GROUP BY company_name
) bc2 ON bc1.company_name = bc2.company_name AND bc1.fetched_at = bc2.max_fetched_at;