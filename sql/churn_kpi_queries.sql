-- Customer Churn & Retention Analytics
-- Assumed tables:
-- telco_churn_clean
-- churn_segment_summary

-- 1. Overall churn KPIs
SELECT
    COUNT(DISTINCT customerid) AS customers,
    SUM(churn_flag) AS churned_customers,
    SUM(churn_flag) / NULLIF(COUNT(DISTINCT customerid), 0) AS churn_rate,
    SUM(monthlycharges) AS monthly_recurring_revenue,
    SUM(monthly_revenue_at_risk) AS monthly_revenue_at_risk
FROM telco_churn_clean;

-- 2. Churn by contract type
SELECT
    contract,
    COUNT(DISTINCT customerid) AS customers,
    SUM(churn_flag) AS churned_customers,
    SUM(churn_flag) / NULLIF(COUNT(DISTINCT customerid), 0) AS churn_rate,
    SUM(monthly_revenue_at_risk) AS revenue_at_risk
FROM telco_churn_clean
GROUP BY contract
ORDER BY churn_rate DESC;

-- 3. Churn by tenure band
SELECT
    tenure_band,
    COUNT(DISTINCT customerid) AS customers,
    SUM(churn_flag) AS churned_customers,
    SUM(churn_flag) / NULLIF(COUNT(DISTINCT customerid), 0) AS churn_rate,
    AVG(monthlycharges) AS avg_monthly_charges
FROM telco_churn_clean
GROUP BY tenure_band
ORDER BY tenure_band;

-- 4. Highest risk customer segments
SELECT
    contract,
    tenure_band,
    internetservice,
    paymentmethod,
    customers,
    churned_customers,
    churn_rate,
    revenue_at_risk
FROM churn_segment_summary
WHERE customers >= 20
ORDER BY revenue_at_risk DESC;

