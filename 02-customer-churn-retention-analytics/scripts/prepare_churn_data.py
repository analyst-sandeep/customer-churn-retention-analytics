from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
PROCESSED = ROOT / "data" / "processed"


def tenure_band(months):
    if months <= 6:
        return "0-6 Months"
    if months <= 12:
        return "7-12 Months"
    if months <= 24:
        return "13-24 Months"
    if months <= 48:
        return "25-48 Months"
    return "49+ Months"


def main():
    if not RAW.exists():
        raise FileNotFoundError(
            f"Raw Kaggle file not found: {RAW}\n"
            "Download it from https://www.kaggle.com/datasets/blastchar/telco-customer-churn "
            "and place the CSV in data/raw."
        )

    PROCESSED.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(RAW)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    df["totalcharges"] = pd.to_numeric(df["totalcharges"], errors="coerce")
    df["totalcharges"] = df["totalcharges"].fillna(0)

    df["churn_flag"] = (df["churn"] == "Yes").astype(int)
    df["tenure_band"] = df["tenure"].apply(tenure_band)
    df["monthly_revenue_at_risk"] = df["monthlycharges"] * df["churn_flag"]
    df["contract_risk_group"] = df["contract"].map(
        {
            "Month-to-month": "High Flex / High Risk",
            "One year": "Medium Commitment",
            "Two year": "High Commitment",
        }
    )

    segment = (
        df.groupby(["contract", "tenure_band", "internetservice", "paymentmethod"])
        .agg(
            customers=("customerid", "nunique"),
            churned_customers=("churn_flag", "sum"),
            avg_monthly_charges=("monthlycharges", "mean"),
            revenue_at_risk=("monthly_revenue_at_risk", "sum"),
        )
        .reset_index()
    )
    segment["churn_rate"] = segment["churned_customers"] / segment["customers"]

    df.to_csv(PROCESSED / "telco_churn_clean.csv", index=False)
    segment.to_csv(PROCESSED / "churn_segment_summary.csv", index=False)
    print(f"Clean rows: {len(df):,}")
    print(f"Segment rows: {len(segment):,}")


if __name__ == "__main__":
    main()

