-- Star Schema for Mutual Fund Analytics
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
