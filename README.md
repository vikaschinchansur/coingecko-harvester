# CoinGecko Cryptocurrency Data Harvester

## What is This Project?

This project is like a **digital assistant** that automatically collects cryptocurrency (digital money like Bitcoin) information from the internet every 60 seconds and saves it for analysis. Think of it as a robot that:
- Checks current Bitcoin and other cryptocurrency prices
- Monitors exchange rates (how much Bitcoin is worth in different currencies)
- Tracks which companies own Bitcoin
- Sends this data to dashboards for real-time visualization

## What Does It Do?

Every 60 seconds, this application:
1. **Fetches cryptocurrency prices** - Gets current prices for Bitcoin, Ethereum, and 9 other major cryptocurrencies
2. **Collects exchange rates** - Finds out how much 1 Bitcoin is worth in 76 different currencies (USD, EUR, JPY, etc.)
3. **Tracks company holdings** - Monitors which public companies (like Tesla, MicroStrategy) own Bitcoin
4. **Stores everything in a database** - Saves all this information for historical tracking
5. **Updates live dashboards** - Sends data to Power BI for real-time charts and graphs

## Technologies Used (In Simple Terms)

- **Python**: The programming language used to write the application (like the language the robot understands)
- **Docker**: A tool that packages everything the application needs to run (like a shipping container for software)
- **MySQL**: A database that stores all the collected data (like a digital filing cabinet)
- **CoinGecko API**: The source of cryptocurrency data (like a news feed for crypto prices)
- **Power BI**: Microsoft's tool for creating visual dashboards (turns numbers into charts)

## Project Structure

```
coingecko-harvester/
├── main.py              # The main program that orchestrates everything
├── api/                 # Code that fetches data from CoinGecko
│   └── coingecko.py    # CoinGecko API client
├── db/                  # Code that saves data to the database
│   └── mysql_client.py # MySQL database operations
├── streaming/           # Code that sends data to Power BI
│   └── powerbi.py      # Power BI streaming client
├── config/              # Application settings
│   └── settings.py     # Configuration management
├── init/                # Database setup files
│   └── schema.sql      # Database table definitions
├── docker-compose.yml   # Instructions for Docker to run everything
├── Dockerfile          # Instructions to build the application container
└── .env                # Secret keys and passwords (never share this!)
```

## Getting Started

### Prerequisites (What You Need First)

1. **Docker Desktop**: Download from [docker.com](https://www.docker.com/products/docker-desktop)
2. **CoinGecko API Key**: Sign up at [coingecko.com](https://www.coingecko.com/en/api) for a free API key
3. **Power BI Account**: Optional - only if you want live dashboards

### Step 1: Clone the Project
```bash
# This downloads the project to your computer
git clone <repository-url>
cd coingecko-harvester
```

### Step 2: Set Up Your Credentials
Create a file named `.env` in the project folder with:
```env
# Your CoinGecko API key
CG_KEY=your_coingecko_api_key_here

# Power BI URLs (optional - get these from Power BI)
PBI_PRICES_PUSH_URL=your_powerbi_prices_url
PBI_EXCHANGE_RATES_URL=your_powerbi_rates_url
PBI_COMPANIES_URL=your_powerbi_companies_url

# Database settings (use these exact values)
MYSQL_HOST=xxxx
MYSQL_PORT=3306
MYSQL_DATABASE=xxxx
MYSQL_USER=xxxx
MYSQL_PASSWORD=xxxx
MYSQL_ROOT_PASSWORD=xxxx
```

### Step 3: Start the Application
```bash
# This starts everything (database + application)
docker compose up --build -d
```

### Step 4: Check If It's Working
```bash
# View the application logs
docker logs coingecko-harvester

# You should see messages like:
# "Fetching crypto prices..."
# "Saved 11 crypto prices to database"
```

## What Data is Collected?

### 1. Cryptocurrency Prices (11 coins)
- Bitcoin (BTC)
- Ethereum (ETH)
- Ripple (XRP)
- Tether (USDT)
- Solana (SOL)
- Binance Coin (BNB)
- USD Coin (USDC)
- Dogecoin (DOGE)
- Cardano (ADA)
- Avalanche (AVAX)
- Shiba Inu (SHIB)

### 2. Exchange Rates
- BTC to 76 different currencies (both traditional money and other cryptocurrencies)

### 3. Company Holdings
- 100+ public companies that own Bitcoin
- Including total holdings, current value, and percentage of total Bitcoin supply

## Database Access

To view the collected data in the database:

```bash
# Connect to MySQL database
mysql -h 127.0.0.1 -P 3306 -u coingecko_user -pcoingecko_pass coingecko_db

# See all tables
SHOW TABLES;

# View latest cryptocurrency prices
SELECT * FROM latest_crypto_prices;

# Count total records collected
SELECT COUNT(*) FROM crypto_prices;

# View top Bitcoin holding companies
SELECT company_name, total_holdings, total_current_value_usd 
FROM bitcoin_companies 
ORDER BY total_holdings DESC 
LIMIT 10;
```

## Stopping the Application

```bash
# Stop the application
docker compose down

# Stop and delete all data (careful!)
docker compose down -v
rm -rf data/mysql/*
```

## Troubleshooting

### Application Not Starting?
1. Check Docker is running: Docker Desktop icon should be in your system tray
2. Check logs: `docker logs coingecko-harvester`

### No Data Being Collected?
1. Verify your CoinGecko API key is correct in `.env`
2. Check internet connection
3. Look for error messages in logs

### Database Connection Issues?
- Use `127.0.0.1` instead of `localhost` when connecting
- Default password is `coingecko_pass`

## Power BI Setup (Optional)

To visualize your data in Power BI:

1. Create streaming datasets in Power BI for:
   - Cryptocurrency prices
   - Exchange rates
   - Company holdings

2. Update the `.env` file with your Power BI Push URLs

3. Create dashboards with real-time tiles showing:
   - Current prices
   - Price trends
   - Top Bitcoin holding companies

See [POWERBI_SETUP.md](POWERBI_SETUP.md) for detailed instructions.

## Security Notes

**Important Security Tips:**
- Never share your `.env` file - it contains passwords!
- Never commit API keys to GitHub
- Keep your Docker Desktop updated
- Use strong passwords for production databases

## Learning Resources

If you want to learn more about the technologies used:

- **Python**: [python.org/about/gettingstarted](https://www.python.org/about/gettingstarted/)
- **Docker**: [docker.com/101-tutorial](https://www.docker.com/101-tutorial/)
- **MySQL**: [dev.mysql.com/doc/mysql-getting-started](https://dev.mysql.com/doc/mysql-getting-started/en/)
- **APIs**: [freecodecamp.org/news/what-is-an-api](https://www.freecodecamp.org/news/what-is-an-api-in-english-please-b880a3214a82/)
- **Cryptocurrency**: [coinbase.com/learn](https://www.coinbase.com/learn)

## Contributing

Want to improve this project? Great! Here's how:
1. Fork the repository (make your own copy)
2. Make your changes
3. Test everything works
4. Submit a pull request (ask to merge your changes)

## License

This project is for educational purposes. Please check CoinGecko's terms of service for API usage limits.

## Getting Help

If you're stuck:
1. Check the Troubleshooting section
2. Read the error messages carefully - they often tell you what's wrong
3. Google the error message - someone else has probably had the same issue
4. Ask for help in the project's Issues section on GitHub

## Success Metrics

You'll know everything is working when:
- Logs show "Fetching all data..." every 60 seconds
- Database tables are filling with data
- No error messages in the logs
- Power BI dashboards (if configured) update automatically

---

**Remember**: Everyone starts as a beginner! Don't be afraid to experiment and learn. The worst that can happen is you delete everything and start fresh - and that's perfectly fine for learning!