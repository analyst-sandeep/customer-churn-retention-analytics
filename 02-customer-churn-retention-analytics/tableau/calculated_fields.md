# Tableau Calculated Fields

Use `data/processed/telco_churn_clean.csv`.

## Churn Flag

```text
IF [churn] = "Yes" THEN 1 ELSE 0 END
```

## Churn Rate

```text
SUM([Churn Flag]) / COUNTD([customerid])
```

## Monthly Revenue At Risk

```text
SUM([monthly_revenue_at_risk])
```

## Customer Count

```text
COUNTD([customerid])
```

## Tenure Band

```text
IF [tenure] <= 6 THEN "0-6 Months"
ELSEIF [tenure] <= 12 THEN "7-12 Months"
ELSEIF [tenure] <= 24 THEN "13-24 Months"
ELSEIF [tenure] <= 48 THEN "25-48 Months"
ELSE "49+ Months"
END
```

## Churn Risk Band

```text
IF [Churn Rate] >= 0.40 THEN "High Risk"
ELSEIF [Churn Rate] >= 0.25 THEN "Medium Risk"
ELSE "Controlled"
END
```

