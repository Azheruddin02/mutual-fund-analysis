import pandas as pd
import numpy as np
import os
from datetime import datetime

# =====================================================
# Create folders
# =====================================================

os.makedirs("data/raw", exist_ok=True)

np.random.seed(42)

# =====================================================
# Generate 40 Mutual Fund Schemes
# =====================================================

fund_houses = [
    "SBI", "HDFC", "ICICI Prudential", "Axis",
    "Kotak", "Nippon India", "Aditya Birla Sun Life",
    "DSP", "Franklin Templeton", "UTI"
]

categories = [
    "Large Cap",
    "Mid Cap",
    "Small Cap",
    "Flexi Cap"
]

schemes = []

amfi_start = 120001

for i in range(40):

    fund = fund_houses[i % len(fund_houses)]

    category = categories[i % len(categories)]

    schemes.append({
        "amfi_code": amfi_start + i,
        "scheme_name": f"{fund} {category} Fund {i+1}",
        "fund_house": fund,
        "category": "Equity",
        "sub_category": category,
        "risk_grade": np.random.choice(
            ["Moderate", "Moderately High", "High"]
        )
    })

fund_master = pd.DataFrame(schemes)

fund_master.to_csv(
    "data/raw/fund_master.csv",
    index=False
)

print("✅ fund_master.csv created")
# =====================================================
# NAV HISTORY
# =====================================================

dates = pd.date_range(
    start="2022-01-01",
    end="2026-12-31",
    freq="D"
)

nav_records = []

for _, scheme in fund_master.iterrows():

    nav = np.random.uniform(20, 100)

    for dt in dates:

        daily_return = np.random.normal(0.0005, 0.01)

        nav *= (1 + daily_return)

        nav_records.append([
            scheme["amfi_code"],
            dt.strftime("%Y-%m-%d"),
            round(nav, 2)
        ])

nav_df = pd.DataFrame(
    nav_records,
    columns=[
        "amfi_code",
        "date",
        "nav"
    ]
)

nav_df.to_csv(
    "data/raw/nav_history.csv",
    index=False
)

print("✅ nav_history.csv created")
# =====================================================
# INVESTOR TRANSACTIONS
# =====================================================

states = [
    "Maharashtra",
    "Karnataka",
    "Telangana",
    "Tamil Nadu",
    "Delhi",
    "Gujarat",
    "Uttar Pradesh",
    "West Bengal",
    "Rajasthan",
    "Kerala"
]

transaction_types = [
    "SIP",
    "Lumpsum",
    "Redemption"
]

transaction_weights = [0.60, 0.25, 0.15]

transactions = []

for i in range(150000):

    investor = f"INV{100000+i}"

    scheme = np.random.choice(
        fund_master["amfi_code"]
    )

    txn_date = pd.Timestamp(np.random.choice(dates))

    txn_type = np.random.choice(
        transaction_types,
        p=transaction_weights
    )

    amount = round(
        np.random.uniform(500,100000),
        2
    )

    nav_value = round(
        np.random.uniform(20,250),
        2
    )

    units = round(
        amount/nav_value,
        3
    )

    transactions.append([
        investor,
        scheme,
        txn_date.strftime("%Y-%m-%d"),
        txn_type,
        amount,
        units,
        "Verified",
        np.random.choice(states)
    ])

transactions = pd.DataFrame(
    transactions,
    columns=[
        "investor_id",
        "amfi_code",
        "transaction_date",
        "transaction_type",
        "amount",
        "units",
        "kyc_status",
        "state"
    ]
)

transactions.to_csv(
    "data/raw/investor_transactions.csv",
    index=False
)

print("✅ investor_transactions.csv created")
# =====================================================
# INVESTOR PROFILE
# =====================================================

genders = [
    "Male",
    "Female",
    "Other"
]

age_groups = [
    "18-25",
    "26-35",
    "36-45",
    "46-60",
    "60+"
]

tiers = [
    "T30",
    "B30"
]

profiles = []

for i in range(20000):

    profiles.append([

        f"INV{100000+i}",

        np.random.choice(age_groups),

        np.random.choice(
            genders,
            p=[0.62,0.36,0.02]
        ),

        np.random.choice(states),

        np.random.choice(
            tiers,
            p=[0.70,0.30]
        )

    ])

profiles = pd.DataFrame(
    profiles,
    columns=[
        "investor_id",
        "age_group",
        "gender",
        "state",
        "city_tier"
    ]
)

profiles.to_csv(
    "data/raw/investor_profile.csv",
    index=False
)

print("✅ investor_profile.csv created")
# =====================================================
# SCHEME PERFORMANCE
# =====================================================

performance = []

for _, scheme in fund_master.iterrows():

    performance.append([

        scheme["amfi_code"],
        scheme["scheme_name"],

        round(np.random.uniform(8,22),2),
        round(np.random.uniform(12,24),2),
        round(np.random.uniform(14,26),2),

        round(np.random.uniform(0.45,1.25),2)

    ])

performance = pd.DataFrame(
    performance,
    columns=[
        "amfi_code",
        "scheme_name",
        "return_1y",
        "return_3y",
        "return_5y",
        "expense_ratio"
    ]
)

performance.to_csv(
    "data/raw/scheme_performance.csv",
    index=False
)

print("✅ scheme_performance.csv created")
# =====================================================
# AUM HISTORY
# =====================================================

months = pd.date_range(
    "2022-01-31",
    "2025-12-31",
    freq="ME"
)

aum = []

for _, scheme in fund_master.iterrows():

    value = np.random.uniform(5000,50000)

    for m in months:

        value *= np.random.uniform(0.98,1.05)

        aum.append([
            scheme["amfi_code"],
            m.strftime("%Y-%m-%d"),
            round(value,2)
        ])

aum = pd.DataFrame(
    aum,
    columns=[
        "amfi_code",
        "date",
        "aum_crore"
    ]
)

aum.to_csv(
    "data/raw/aum_history.csv",
    index=False
)

print("✅ aum_history.csv created")
# =====================================================
# PORTFOLIO HOLDINGS
# =====================================================

sectors = [
    "Banking",
    "IT",
    "Pharma",
    "Auto",
    "FMCG",
    "Energy",
    "Capital Goods",
    "Financial Services",
    "Metals",
    "Infrastructure"
]

holdings = []

for _, scheme in fund_master.iterrows():

    weights = np.random.dirichlet(np.ones(len(sectors))) * 100

    for sector, weight in zip(sectors, weights):

        holdings.append([
            scheme["amfi_code"],
            sector,
            round(weight,2)
        ])

holdings = pd.DataFrame(
    holdings,
    columns=[
        "amfi_code",
        "sector",
        "weight"
    ]
)

holdings.to_csv(
    "data/raw/portfolio_holdings.csv",
    index=False
)

print("✅ portfolio_holdings.csv created")
benchmark = pd.DataFrame({

    "date": months.strftime("%Y-%m-%d"),

    "nifty_return": np.random.uniform(-8,18,len(months))

})

benchmark.to_csv(
    "data/raw/benchmark_index.csv",
    index=False
)
category = []

for c in categories:

    for m in months:

        category.append([

            c,

            m.strftime("%Y-%m"),

            round(np.random.uniform(-6,20),2)

        ])

category = pd.DataFrame(
    category,
    columns=[
        "category",
        "month",
        "avg_return"
    ]
)

category.to_csv(
    "data/raw/category_returns.csv",
    index=False
)

print("✅ category_returns.csv created")
fund_master.to_csv(
    "data/raw/scheme_master.csv",
    index=False
)

print("✅ scheme_master.csv created")
print("\n🎉 ALL DATASETS GENERATED SUCCESSFULLY!")