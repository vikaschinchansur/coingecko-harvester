# Power BI Cryptocurrency Dashboard Creation Guide

## Prerequisites
- Access to Power BI Service (app.powerbi.com)
- Your 3 streaming datasets already receiving data from the Python harvester:
  1. **coingecko_prices_dataset** - Real-time BTC and ETH prices
  2. **coingecko_btc_exchange_rates_datasets** - Bitcoin exchange rates in multiple currencies
  3. **coingecko_btc_company_holdings** - Corporate Bitcoin holdings data
- Power BI Desktop (optional, for advanced features)

## Dashboard Overview
We'll create a comprehensive cryptocurrency monitoring dashboard using your 3 datasets:

### Dashboard 1: Price Monitor (coingecko_prices_dataset)
- Real-time BTC and ETH price cards
- Price trend line charts
- Price comparison visualizations

### Dashboard 2: Global Exchange Rates (coingecko_btc_exchange_rates_datasets)
- Multi-currency exchange rate cards
- Currency strength comparison charts
- Geographic heat maps (if coordinates available)

### Dashboard 3: Institutional Holdings (coingecko_btc_company_holdings)
- Company holdings bar charts
- Holdings distribution pie charts
- Top holders leaderboard

### Dashboard 4: Combined Master Dashboard
- Key metrics from all three datasets
- Cross-dataset correlations
- Comprehensive market overview

---

## Step 1: Access Your Streaming Datasets

1. **Log into Power BI Service**
   - Navigate to https://app.powerbi.com
   - Sign in with your Microsoft account

2. **Locate Your Datasets**
   - Click on "Workspaces" in the left navigation
   - Select your workspace
   - Find your 3 streaming datasets (they should show with a lightning bolt icon)

---

## Step 2: Create a New Dashboard

1. **Initialize Dashboard**
   - In your workspace, click "+ New" → "Dashboard"
   - Name it "Cryptocurrency Real-Time Monitor" (or your preferred name)
   - Click "Create"

---

## Step 3: Create Visualizations

### Visualization 1: Real-Time Price Cards (Big Numbers)

**Dataset to Use**: `coingecko_prices_dataset`
**Purpose**: Display current BTC and ETH prices prominently

1. **Add Tile from Report**
   - Click "Edit" → "+ Add a tile"
   - Select "Custom Streaming Data"
   - Choose **coingecko_prices_dataset**
   - Click "Next"

2. **Configure Bitcoin Price Card**
   - Visualization Type: **Card**
   - Fields:
     - Value: `btc_price`
   - Display Settings:
     - Title: "Bitcoin (USD)"
     - Display units: Currency
     - Decimal places: 2
     - Text size: Extra large
   - Click "Apply"

3. **Repeat for Ethereum**
   - Create another card tile
   - Dataset: **coingecko_prices_dataset**
   - Value: `eth_price`
   - Title: "Ethereum (USD)"

**Visual Impact**: Large, easy-to-read numbers showing live prices

---

### Visualization 2: Price Trend Line Chart

**Dataset to Use**: `coingecko_prices_dataset`
**Purpose**: Show price movements over time

1. **Create Line Chart**
   - Add new tile → Custom Streaming Data
   - Choose **coingecko_prices_dataset**
   - Visualization Type: **Line chart**
   
2. **Configure Fields**
   - Axis: `timestamp`
   - Values: 
     - `btc_price` (Line 1)
     - `eth_price` (Line 2)
   - Legend: On
   
3. **Display Settings**
   - Title: "BTC vs ETH Price Trends (Last Hour)"
   - Time window: 60 minutes
   - Y-Axis: 
     - Start: Auto
     - End: Auto
     - Display units: Thousands
   - Line style: Smooth
   - Data labels: Off (for cleaner view)
   - Grid lines: On

**Teaching Point**: Shows correlation and divergence between assets

---

### Visualization 3: Exchange Rates Matrix

**Dataset to Use**: `coingecko_btc_exchange_rates_datasets`
**Purpose**: Display Bitcoin value in multiple currencies

1. **Create Multi-Currency Cards**
   - Add tile → Custom Streaming Data
   - Choose **coingecko_btc_exchange_rates_datasets**
   - Visualization Type: **Card**
   
2. **Configure Exchange Rate Cards** (Create multiple):
   - **EUR Card**:
     - Value: `btc_eur`
     - Title: "BTC/EUR"
     - Display units: Currency
   - **GBP Card**:
     - Value: `btc_gbp`
     - Title: "BTC/GBP"
   - **JPY Card**:
     - Value: `btc_jpy`
     - Title: "BTC/JPY"
   - **CNY Card**:
     - Value: `btc_cny`
     - Title: "BTC/CNY"

**Teaching Point**: Shows global perspective of Bitcoin valuation

---

### Visualization 4: Company Holdings Bar Chart

**Dataset to Use**: `coingecko_btc_company_holdings`
**Purpose**: Display corporate Bitcoin holdings comparison

1. **Create Holdings Chart**
   - Add tile → Custom Streaming Data
   - Choose **coingecko_btc_company_holdings**
   - Visualization Type: **Clustered bar chart**
   
2. **Configure Fields**
   - Category: `company_name`
   - Values: `total_holdings`
   
3. **Display Settings**
   - Title: "Top Corporate BTC Holdings"
   - Sort: Descending by value
   - Data labels: On
   - Display top 10 companies

**Educational Value**: Shows institutional adoption and investment scale

---

### Visualization 5: Combined Dashboard View

**Purpose**: Create a comprehensive view using all three datasets

1. **Multi-Dataset Line Chart**
   - Add tile → Custom Streaming Data
   - Choose **coingecko_prices_dataset**
   - Visualization Type: **Line chart**
   
2. **Configure Fields**
   - Axis: `timestamp`
   - Values:
     - `btc_price` (from prices dataset)
     - `eth_price` (from prices dataset)
   
3. **Add Overlay Information**
   - Create text tiles showing:
     - Total corporate holdings value (holdings × current BTC price)
     - Exchange rate spreads
   - Title: "Comprehensive Crypto Dashboard"
   - Time window: Last 60 minutes

---

## Step 4: Add KPI Tiles

### Dataset-Specific KPI Tiles

### KPI Tile 1: Price Summary (from coingecko_prices_dataset)

1. **Create Price KPI Tiles**
   - Dataset: **coingecko_prices_dataset**
   - Add tile → Text box or Card
   - Content:
     ```
     📊 Live Prices
     BTC: [Use btc_price field]
     ETH: [Use eth_price field]
     Last Update: [timestamp]
     ```

### KPI Tile 2: Exchange Rate Summary (from coingecko_btc_exchange_rates_datasets)

1. **Create Exchange Rate KPIs**
   - Dataset: **coingecko_btc_exchange_rates_datasets**
   - Add multiple small cards showing:
     - BTC/USD baseline
     - Strongest currency pair
     - Weakest currency pair
   - Use conditional formatting for color coding

### KPI Tile 3: Holdings Summary (from coingecko_btc_company_holdings)

1. **Create Holdings KPI**
   - Dataset: **coingecko_btc_company_holdings**
   - Add tile → Card or custom visual
   - Show:
     - Total BTC held by companies
     - Number of companies
     - Average holdings per company
     - Largest holder name and amount

---

## Step 5: Dashboard Layout Best Practices

### Recommended Layout Structure:

```
+------------------+------------------+------------------+------------------+
|  BTC Price Card  |  ETH Price Card  | BTC/EUR Card    | BTC/GBP Card     |
| (prices_dataset) | (prices_dataset) | (exchange_rates)| (exchange_rates) |
+------------------+------------------+------------------+------------------+
|              Price Trend Line Chart (Wide)                                |
|                  (coingecko_prices_dataset)                               |
+----------------------------------------------------------------------------+
|     Exchange Rates Matrix      |     Company Holdings Bar Chart           |
| (btc_exchange_rates_datasets)  |    (btc_company_holdings)               |
+--------------------------------+------------------------------------------+
| Price KPIs | Exchange KPIs | Holdings KPIs | Update Status               |
+----------------------------------------------------------------------------+
```

### Design Tips:

1. **Color Scheme**
   - Bitcoin: Orange (#F7931A)
   - Ethereum: Purple/Blue (#627EEA)
   - Background: Dark theme for better contrast

2. **Spacing**
   - Leave small gaps between tiles
   - Group related visualizations
   - Maintain visual hierarchy (important info at top)

3. **Mobile Optimization**
   - Pin tiles in order of importance
   - Test on mobile view
   - Ensure text is readable

---

## Step 6: Advanced Features

### 1. Add Alerts (Pro/Premium)
- Set alerts when BTC > $100,000
- Alert when ETH < $3,000
- Rapid change notifications (>5% in 5 minutes)

### 2. Add Q&A Visual
- Natural language queries
- "What is the current bitcoin price?"
- "Show ethereum trend for last hour"

### 3. Create Bookmarks
- Save different time ranges
- Save different chart types
- Quick view switching

---

## Step 7: Sharing and Presentation

### For Students:

1. **Share Dashboard**
   - Click "Share" button
   - Generate shareable link
   - Set permissions (view only for students)

2. **Embed in Teams/PowerPoint**
   - File → Embed → Generate embed code
   - Paste in Microsoft Teams channel
   - Add to PowerPoint for presentations

3. **Schedule Refresh** (if using non-streaming data)
   - Settings → Scheduled refresh
   - Set to every 5 minutes minimum

---

## Teaching Points to Highlight

1. **Real-Time Data Visualization**
   - Importance of live data in financial markets
   - Streaming vs batch processing
   - Update frequency considerations

2. **Visual Design Principles**
   - Color usage for quick comprehension
   - Chart type selection based on data story
   - Information hierarchy

3. **Business Intelligence Concepts**
   - KPIs and metrics
   - Trend analysis
   - Comparative visualization
   - Dashboard vs reports

4. **Technical Skills Demonstrated**
   - API integration (via Python harvester)
   - Streaming datasets
   - Power BI Service navigation
   - Visual customization

---

## Troubleshooting Common Issues

### Issue 1: Data Not Updating
- **Check**: Python script is running
- **Verify**: Streaming dataset is receiving data
- **Solution**: Check dataset settings, ensure "Historic data analysis" is ON

### Issue 2: Visuals Not Loading
- **Check**: Browser compatibility (use Edge/Chrome)
- **Clear**: Browser cache
- **Refresh**: Dashboard manually

### Issue 3: Incorrect Values
- **Verify**: Data format in Python script
- **Check**: Field mappings in visualizations
- **Ensure**: Correct aggregations (Sum, Average, Last)

---

## Demo Script for Students

1. **Opening** (2 mins)
   - Show live dashboard
   - Explain cryptocurrency context
   - Highlight real-time aspect

2. **Technical Overview** (3 mins)
   - Python → API → Power BI flow
   - Streaming dataset concept
   - Update frequency

3. **Visual Tour** (5 mins)
   - Explain each chart type
   - Why each visualization was chosen
   - Interactivity demonstration

4. **Business Value** (2 mins)
   - Trading decisions
   - Market monitoring
   - Pattern recognition

5. **Q&A and Hands-On** (8 mins)
   - Let students explore
   - Show customization options
   - Discuss improvements

---

## Dataset Field Reference

### coingecko_prices_dataset Fields:
- `timestamp` - Date/time of price capture
- `btc_price` - Bitcoin price in USD
- `eth_price` - Ethereum price in USD

### coingecko_btc_exchange_rates_datasets Fields:
- `timestamp` - Date/time of exchange rate capture
- `btc_usd` - Bitcoin price in US Dollars
- `btc_eur` - Bitcoin price in Euros
- `btc_gbp` - Bitcoin price in British Pounds
- `btc_jpy` - Bitcoin price in Japanese Yen
- `btc_cny` - Bitcoin price in Chinese Yuan
- Additional currency pairs as configured

### coingecko_btc_company_holdings Fields:
- `timestamp` - Date/time of holdings data
- `company_name` - Name of the company
- `total_holdings` - Total BTC held
- `country` - Company's country
- `percentage_of_supply` - Percentage of total BTC supply

---

## Next Steps and Extensions

1. **Add More Cryptocurrencies**
   - Expand to top 10 coins
   - Create comparison matrix
   - Market cap visualizations

2. **Historical Analysis**
   - Add SQL database for history
   - Create trend predictions
   - Moving averages

3. **Advanced Analytics**
   - Volatility indicators
   - Correlation matrices
   - Price predictions (with R/Python visuals)

4. **Alerts and Actions**
   - Power Automate integration
   - Email/SMS notifications
   - Automated trading signals (demo only)

---

## Resources for Students

- [Power BI Documentation](https://docs.microsoft.com/en-us/power-bi/)
- [Streaming Datasets Guide](https://docs.microsoft.com/en-us/power-bi/connect-data/service-real-time-streaming)
- [DAX Functions Reference](https://docs.microsoft.com/en-us/dax/)
- [Power BI Community](https://community.powerbi.com/)

---

## Assessment Ideas

1. **Practical Test**
   - Create a new visualization
   - Modify existing dashboard
   - Explain chart selection

2. **Project Extension**
   - Add a third cryptocurrency
   - Create mobile-optimized view
   - Implement custom KPIs

3. **Presentation**
   - Present dashboard to class
   - Explain design decisions
   - Demonstrate real-time updates

---

**Remember**: The goal is not just to display data, but to tell a story that helps viewers make informed decisions about cryptocurrency markets. Each visualization should serve a specific purpose and contribute to the overall narrative of market behavior.