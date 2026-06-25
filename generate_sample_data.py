import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

os.makedirs('data/raw', exist_ok=True)
np.random.seed(42)

amfi_codes = [125497, 119551, 120503, 118632, 119092, 120841]
scheme_names = ['HDFC Top 100 Direct', 'SBI Bluechip Fund', 'ICICI Pru Bluechip', 
                'Nippon India Large Cap', 'Axis Bluechip Fund', 'Kotak Bluechip Fund']
fund_houses = ['HDFC', 'SBI', 'ICICI Prudential', 'Nippon India', 'Axis', 'Kotak']

print("Generating 10 sample CSV files...\n")

# 1. fund_master.csv
fund_master = pd.DataFrame({
    'amfi_code': amfi_codes,
    'scheme_name': scheme_names,
    'fund_house': fund_houses,
    'category': ['Equity']*6,
    'sub_category': ['Large Cap']*6,
    'risk_grade': ['Moderate', 'Moderate', 'Moderate', 'High', 'Moderate', 'Moderate']
})
fund_master.to_csv('data/raw/fund_master.csv', index=False)
print("✅ fund_master.csv created")

# 2. nav_history.csv
dates = pd.date_range(end=datetime.today(), periods=180, freq='D')
nav_data = []
for code in amfi_codes:
    for date in dates:
        nav = round(np.random.uniform(40, 180), 2)
        nav_data.append([code, date.strftime('%Y-%m-%d'), nav])
nav_df = pd.DataFrame(nav_data, columns=['amfi_code', 'date', 'nav'])
nav_df.to_csv('data/raw/nav_history.csv', index=False)
print("✅ nav_history.csv created")

# 3. investor_transactions.csv
trans_data = []
for i in range(5000):
    code = np.random.choice(amfi_codes)
    date = datetime.today() - timedelta(days=np.random.randint(1, 365))
    txn_type = np.random.choice(['SIP', 'Lumpsum', 'Redemption'])
    amount = round(np.random.uniform(500, 100000), 2)
    units = round(amount / np.random.uniform(80, 150), 3)
    kyc = np.random.choice(['Verified', 'Pending', 'Verified'])
    trans_data.append([f'INV{1000+i}', code, date.strftime('%Y-%m-%d'), txn_type, amount, units, kyc, 'Maharashtra'])
pd.DataFrame(trans_data, columns=['investor_id','amfi_code','transaction_date','transaction_type',
                                  'amount','units','kyc_status','state']).to_csv('data/raw/investor_transactions.csv', index=False)
print("✅ investor_transactions.csv created")

# 4. scheme_performance.csv
perf = pd.DataFrame({
    'amfi_code': amfi_codes,
    'scheme_name': scheme_names,
    'return_1y': [12.4, 14.8, 13.2, 18.5, 11.9, 13.7],
    'return_3y': [15.2, 16.8, 14.9, 19.1, 14.3, 15.6],
    'return_5y': [14.1, 15.3, 13.8, 17.2, 13.5, 14.8],
    'expense_ratio': [0.85, 0.92, 0.78, 1.05, 0.65, 0.88]
})
perf.to_csv('data/raw/scheme_performance.csv', index=False)
print("✅ scheme_performance.csv created")

# 5. aum_history.csv
aum_data = []
for code in amfi_codes:
    for i in range(24):
        date = datetime(2023, 1, 1) + timedelta(days=30*i)
        aum = round(np.random.uniform(8000, 45000), 2)
        aum_data.append([code, date.strftime('%Y-%m-%d'), aum])
pd.DataFrame(aum_data, columns=['amfi_code','date','aum_crore']).to_csv('data/raw/aum_history.csv', index=False)
print("✅ aum_history.csv created")

# 6 to 10: Additional supporting files
pd.DataFrame({'amfi_code': amfi_codes, 'fund_house': fund_houses, 'launch_date': '2018-01-01'}).to_csv('data/raw/scheme_master.csv', index=False)
pd.DataFrame({'investor_id': [f'INV{1000+i}' for i in range(100)], 'age': np.random.randint(25,65,100), 'state': 'Maharashtra'}).to_csv('data/raw/investor_profile.csv', index=False)
pd.DataFrame({'amfi_code': amfi_codes, 'stock_name': ['Reliance','HDFC Bank','ICICI Bank','Infosys','TCS','L&T'], 'holding_pct': [8.2,7.1,6.5,5.8,4.9,4.2]}).to_csv('data/raw/portfolio_holdings.csv', index=False)
pd.DataFrame({'date': pd.date_range('2023-01-01', periods=24, freq='M').strftime('%Y-%m-%d'), 'nifty_return': np.random.uniform(8,18,24)}).to_csv('data/raw/benchmark_index.csv', index=False)
pd.DataFrame({'category': ['Large Cap']*12, 'month': pd.date_range('2023-01-01', periods=12, freq='M').strftime('%Y-%m'), 'avg_return': np.random.uniform(10,20,12)}).to_csv('data/raw/category_returns.csv', index=False)

print("\n🎉 All 10 CSV files have been successfully generated in data/raw/ folder!")
print("\nYou can now run Day 1 and Day 2 scripts.")
