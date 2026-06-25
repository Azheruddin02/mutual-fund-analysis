# Mutual Fund Data Dictionary (Day 2)

## Cleaned Datasets (data/processed/)
- 
av_history_clean.csv: Dates parsed, NAV forward-filled, duplicates removed, NAV > 0
- investor_transactions_clean.csv: Standardized transaction_type (SIP/Lumpsum/Redemption), amount > 0, valid KYC
- scheme_performance_clean.csv: Numeric returns, expense_ratio between 0.1%–2.5%

## Star Schema (bluestock_mf.db)
- **dim_fund**: Fund master (amfi_code as bridge)
- **dim_date**: Date dimension
- **fact_nav**: Historical NAV
- **fact_transactions**: Investor transactions
- **fact_performance**: Returns and expense ratio
- **fact_aum**: Assets Under Management

**Primary Keys**: fund_key, date_key, etc.
**Foreign Keys**: amfi_code, date_key linking facts to dimensions.
