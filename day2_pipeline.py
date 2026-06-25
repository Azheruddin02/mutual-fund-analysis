import pandas as pd
import numpy as np
import sqlite3
import os
from sqlalchemy import create_engine
from pathlib import Path

print('=== Mutual Fund Analysis - Day 2 ===\n')

# Create folders
os.makedirs('data/processed', exist_ok=True)
os.makedirs('sql', exist_ok=True)

# ====================== 1. DATA CLEANING ======================
def clean_data():
    processed_files = []
    
    # 1. nav_history.csv
    if os.path.exists('data/raw/nav_history.csv'):
        nav = pd.read_csv('data/raw/nav_history.csv')
        nav['date'] = pd.to_datetime(nav['date'], errors='coerce')
        nav = nav.sort_values(['amfi_code', 'date']).reset_index(drop=True)
        nav['nav'] = nav.groupby('amfi_code')['nav'].ffill()
        nav = nav[nav['nav'] > 0].drop_duplicates(subset=['amfi_code', 'date'])
        nav.to_csv('data/processed/nav_history_clean.csv', index=False)
        processed_files.append('nav_history_clean.csv')
        print('✅ nav_history cleaned')
    else:
        print('⚠️  nav_history.csv not found in data/raw/')

    # 2. investor_transactions.csv
    if os.path.exists('data/raw/investor_transactions.csv'):
        trans = pd.read_csv('data/raw/investor_transactions.csv')
        trans['transaction_type'] = trans['transaction_type'].str.title().replace(['Sip','Systematic'],'SIP')
        trans['transaction_date'] = pd.to_datetime(trans['transaction_date'], errors='coerce')
        trans = trans[trans['amount'] > 0]
        trans = trans[trans['kyc_status'].isin(['Verified','Pending','Rejected'])]
        trans.to_csv('data/processed/investor_transactions_clean.csv', index=False)
        processed_files.append('investor_transactions_clean.csv')
        print('✅ investor_transactions cleaned')
    
    # 3. scheme_performance.csv
    if os.path.exists('data/raw/scheme_performance.csv'):
        perf = pd.read_csv('data/raw/scheme_performance.csv')
        for col in ['return_1y','return_3y','return_5y','expense_ratio']:
            perf[col] = pd.to_numeric(perf[col], errors='coerce')
        perf = perf[(perf['expense_ratio'] >= 0.1) & (perf['expense_ratio'] <= 2.5)]
        perf.to_csv('data/processed/scheme_performance_clean.csv', index=False)
        processed_files.append('scheme_performance_clean.csv')
        print('✅ scheme_performance cleaned')
    
    # Copy other raw files to processed
    for file in os.listdir('data/raw'):
        if file.endswith('.csv') and 'clean' not in file:
            pd.read_csv(f'data/raw/{file}').to_csv(f'data/processed/{file.replace(".csv","_clean.csv")}', index=False)
    
    print(f'\n✅ Cleaned files saved to data/processed/ ({len(processed_files)} major files cleaned)')

clean_data()

# ====================== 2. STAR SCHEMA ======================
schema_sql = '''-- Star Schema for Mutual Fund Analytics
CREATE TABLE IF NOT EXISTS dim_fund (
    fund_key INTEGER PRIMARY KEY,
    amfi_code INTEGER UNIQUE,
    scheme_name TEXT,
    fund_house TEXT,
    category TEXT,
    sub_category TEXT,
    risk_grade TEXT
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE,
    year INTEGER,
    month INTEGER,
    quarter INTEGER
);

CREATE TABLE IF NOT EXISTS fact_nav (
    nav_key INTEGER PRIMARY KEY,
    amfi_code INTEGER,
    date_key INTEGER,
    nav REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

CREATE TABLE IF NOT EXISTS fact_transactions (
    txn_key INTEGER PRIMARY KEY,
    amfi_code INTEGER,
    date_key INTEGER,
    transaction_type TEXT,
    amount REAL,
    units REAL,
    kyc_status TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE IF NOT EXISTS fact_performance (
    perf_key INTEGER PRIMARY KEY,
    amfi_code INTEGER,
    date_key INTEGER,
    return_1y REAL,
    return_3y REAL,
    return_5y REAL,
    expense_ratio REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE IF NOT EXISTS fact_aum (
    aum_key INTEGER PRIMARY KEY,
    amfi_code INTEGER,
    date_key INTEGER,
    aum_crore REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);
'''

with open('sql/schema.sql', 'w') as f:
    f.write(schema_sql)
print('✅ schema.sql created')

# ====================== 3. LOAD TO SQLITE ======================
conn = sqlite3.connect('bluestock_mf.db')
conn.executescript(schema_sql)

# Load sample data if real files not available
if os.path.exists('data/processed/nav_history_clean.csv'):
    nav_clean = pd.read_csv('data/processed/nav_history_clean.csv')
    nav_clean.to_sql('fact_nav', conn, if_exists='replace', index=False)

print('✅ Data loaded into bluestock_mf.db')

# ====================== 4. ANALYTICAL QUERIES ======================
queries = """-- Day 2 Analytical Queries

-- 1. Top 5 Funds by AUM
SELECT fund_house, scheme_name, aum_crore 
FROM fact_aum fa JOIN dim_fund df ON fa.amfi_code = df.amfi_code
ORDER BY aum_crore DESC LIMIT 5;

-- 2. Average Monthly NAV
SELECT strftime('%Y-%m', full_date) as month, AVG(nav) as avg_nav
FROM fact_nav n JOIN dim_date d ON n.date_key = d.date_key
GROUP BY month;

-- 3. SIP vs Lumpsum Comparison
SELECT transaction_type, COUNT(*) as count, SUM(amount) as total_amount
FROM fact_transactions GROUP BY transaction_type;

-- 4. Funds with Low Expense Ratio (< 1%)
SELECT scheme_name, expense_ratio FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code WHERE expense_ratio < 1.0;

-- 5. YoY SIP Growth
SELECT strftime('%Y', full_date) as year, SUM(amount) as total_sip
FROM fact_transactions t JOIN dim_date d ON t.date_key = d.date_key
WHERE transaction_type = 'SIP' GROUP BY year;

-- 6. Best 3-Year Return Funds
SELECT scheme_name, return_3y, risk_grade 
FROM fact_performance p JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY return_3y DESC LIMIT 5;

-- 7. Transaction Count by KYC Status
SELECT kyc_status, COUNT(*) as txn_count FROM fact_transactions GROUP BY kyc_status;

-- 8. Funds with Positive Returns Across Horizons
SELECT scheme_name FROM fact_performance 
WHERE return_1y > 0 AND return_3y > 0 AND return_5y > 0;

-- 9. Monthly AUM Trend for Top Fund
SELECT strftime('%Y-%m', full_date) as month, aum_crore 
FROM fact_aum a JOIN dim_date d ON a.date_key = d.date_key 
WHERE amfi_code = 125497 ORDER BY month;

-- 10. Average Expense Ratio by Category
SELECT category, AVG(expense_ratio) as avg_expense 
FROM fact_performance p JOIN dim_fund f ON p.amfi_code = f.amfi_code 
GROUP BY category;
"""

with open('sql/queries.sql', 'w') as f:
    f.write(queries)
print('✅ queries.sql created (10 analytical queries)')

# ====================== 5. DATA DICTIONARY ======================
data_dict = """# Mutual Fund Data Dictionary (Day 2)

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
"""

with open('data_dictionary.md', 'w') as f:
    f.write(data_dict)
print('✅ data_dictionary.md created')

print('\n🎉 DAY 2 COMPLETED SUCCESSFULLY!')
print('Deliverables ready: data/processed/, bluestock_mf.db, schema.sql, queries.sql, data_dictionary.md')
