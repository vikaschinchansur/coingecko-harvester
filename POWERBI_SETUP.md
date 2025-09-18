# Power BI Streaming Dataset Setup Guide

This guide explains how to set up Power BI streaming datasets for the CoinGecko Harvester application.

## Overview

The application pushes data to Power BI streaming datasets in real-time. You'll need to create three separate streaming datasets to handle different data types:

1. **Cryptocurrency Prices** - Real-time crypto price updates
2. **BTC Exchange Rates** - Bitcoin to currency exchange rates
3. **Bitcoin Company Holdings** - Public companies holding Bitcoin

## Prerequisites

- Power BI Pro or Premium account
- Access to create streaming datasets in your Power BI workspace

## Creating Streaming Datasets

### 1. Cryptocurrency Prices Dataset

1. Navigate to your Power BI workspace
2. Click **+ New** → **Streaming dataset**
3. Choose **API** and click **Next**
4. Configure the dataset:
   - **Dataset name**: `CoinGecko Crypto Prices`
   - **Fields**:
     - `asset` (Text)
     - `price_usd` (Number)
     - `price_aud` (Number)
     - `timestamp` (DateTime)
     - `exchange` (Text)
     - `source` (Text)
     - `volume_24h` (Number)
     - `change_pct_24h` (Number)
     - `market_cap_usd` (Number)
     - `ingested_at` (DateTime)
5. Enable **Historic data analysis**
6. Click **Create**
7. Copy the **Push URL** for your .env file

### 2. BTC Exchange Rates Dataset

1. Create a new streaming dataset
2. Configure:
   - **Dataset name**: `BTC Exchange Rates`
   - **Fields**:
     - `base_currency` (Text)
     - `target_currency` (Text)
     - `exchange_rate` (Number)
     - `currency_type` (Text)
     - `currency_name` (Text)
     - `timestamp` (DateTime)
3. Enable **Historic data analysis**
4. Create and copy the Push URL

### 3. Bitcoin Company Holdings Dataset

1. Create a new streaming dataset
2. Configure:
   - **Dataset name**: `Bitcoin Company Holdings`
   - **Fields**:
     - `company_name` (Text)
     - `ticker_symbol` (Text)
     - `country` (Text)
     - `total_btc` (Number)
     - `total_value_usd` (Number)
     - `percent_of_supply` (Number)
     - `timestamp` (DateTime)
3. Enable **Historic data analysis**
4. Create and copy the Push URL

## Environment Configuration

Update your `.env` file with the appropriate Push URLs:

```bash
# Primary crypto prices dataset
PBI_PRICES_PUSH_URL=https://api.powerbi.com/beta/[workspace-id]/datasets/[dataset-id]/rows?key=[key]

# Additional datasets (if using separate endpoints)
PBI_EXCHANGE_RATES_URL=https://api.powerbi.com/beta/[workspace-id]/datasets/[dataset-id]/rows?key=[key]
PBI_COMPANIES_URL=https://api.powerbi.com/beta/[workspace-id]/datasets/[dataset-id]/rows?key=[key]
```

## Creating Real-time Dashboards

### Crypto Price Dashboard

1. In your workspace, click **+ New** → **Dashboard**
2. Click **+ Add tile** → **Custom Streaming Data**
3. Select your crypto prices dataset
4. Choose visualization type (Line chart recommended)
5. Configure:
   - **Axis**: `timestamp`
   - **Values**: `price_usd`
   - **Legend**: `asset`
6. Set time window (e.g., last 60 minutes)

### Exchange Rates Dashboard

1. Add a new tile to your dashboard
2. Select BTC Exchange Rates dataset
3. Use a Card visualization for current rates
4. Or use a Line chart to show rate trends

### Company Holdings Dashboard

1. Add a new tile
2. Select Bitcoin Company Holdings dataset
3. Use a Table or Bar chart visualization
4. Sort by `total_value_usd` descending

## Data Retention

- Streaming datasets retain data for 1 hour by default
- With **Historic data analysis** enabled, data is retained for 200,000 rows
- Consider implementing data archival for long-term storage

## Monitoring

### Power BI Push Logs

The application logs all Power BI push attempts to MySQL. Query the `powerbi_push_logs` table to monitor:

```sql
-- Check recent push status
SELECT status, COUNT(*) as count, MAX(created_at) as last_push
FROM powerbi_push_logs
WHERE created_at > NOW() - INTERVAL 1 HOUR
GROUP BY status;

-- View recent failures
SELECT * FROM powerbi_push_logs
WHERE status = 'failure'
ORDER BY created_at DESC
LIMIT 10;
```

## Troubleshooting

### Common Issues

1. **401 Unauthorized**: Check your Push URL is correct and not expired
2. **400 Bad Request**: Verify data format matches dataset schema
3. **429 Too Many Requests**: Power BI has rate limits (max 1 request/second per dataset)
4. **503 Service Unavailable**: Power BI service issue, implement retry logic

### Rate Limiting

The application implements these strategies:
- Batches multiple rows in a single push
- Implements 5-second intervals between price updates
- Fetches additional data every 100 seconds

## Best Practices

1. **Use separate datasets** for different data types to avoid schema conflicts
2. **Enable historic data analysis** for all datasets
3. **Set up alerts** in Power BI for anomalies
4. **Monitor push logs** regularly for failures
5. **Implement data archival** for long-term analysis
6. **Use row-level security** if sharing dashboards

## API Limitations

- Maximum 1 million rows pushed per hour per dataset
- Maximum 10,000 rows per single POST request
- Maximum 75 columns per dataset
- Maximum 75 tables per dataset

## Support

For issues related to:
- **Application**: Check logs in MySQL `powerbi_push_logs` table
- **Power BI**: Visit [Power BI Support](https://powerbi.microsoft.com/support/)
- **CoinGecko API**: Check [CoinGecko API Status](https://status.coingecko.com/)