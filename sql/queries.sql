-- Day 2 Analytical Queries

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
