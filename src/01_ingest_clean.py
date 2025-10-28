#!/usr/bin/env python
"""
Load the raw e‑commerce customer behaviour CSV, clean and enrich it, and save the
result to `data/processed/customers_clean.csv`.

Tasks performed:
  * Enforce data types for numeric and boolean columns
  * Standardise string columns to title case
  * Fill missing satisfaction values with "Unknown"
  * Derive the following fields:
      - is_high_value: True if total_spend >= 1000
      - recency_band: categorical bin of days_since_last_purchase
      - discount_label: "Discount" or "No Discount" based on discount_applied
      - purchase_date: date of last purchase (today minus days_since_last_purchase)
"""
import os
from datetime import datetime, timedelta
import pandas as pd


def ingest_and_clean(input_path: str, output_path: str) -> pd.DataFrame:
    """Read the raw CSV, clean and enrich it, then write to output_path."""
    df = pd.read_csv(input_path)
    # Rename columns to snake_case
    df = df.rename(columns={
        'Customer ID': 'customer_id',
        'Gender': 'gender',
        'Age': 'age',
        'City': 'city',
        'Membership Type': 'membership_type',
        'Total Spend': 'total_spend',
        'Items Purchased': 'items_purchased',
        'Average Rating': 'avg_rating',
        'Discount Applied': 'discount_applied',
        'Days Since Last Purchase': 'days_since_last_purchase',
        'Satisfaction Level': 'satisfaction_level'
    })
    # Enforce dtypes
    df['age'] = df['age'].astype(int)
    df['items_purchased'] = df['items_purchased'].astype(int)
    df['total_spend'] = df['total_spend'].astype(float)
    df['avg_rating'] = df['avg_rating'].astype(float)
    # Ensure boolean for discount
    # Some CSV parsers may read booleans as strings; convert accordingly
    if df['discount_applied'].dtype != bool:
        df['discount_applied'] = df['discount_applied'].astype(str).str.strip().str.lower().map({'true': True, 'false': False})
    # Title‑case string fields
    for col in ['gender', 'city', 'membership_type', 'satisfaction_level']:
        df[col] = df[col].astype(str).str.title()
    # Fill missing satisfaction
    df['satisfaction_level'] = df['satisfaction_level'].replace({'': None}).fillna('Unknown')
    # Derived flags and bands
    df['is_high_value'] = df['total_spend'] >= 1000
    # Recency bands: 0–14, 15–30, 31–60, 60+
    bins = [-1, 14, 30, 60, float('inf')]
    labels = ['0-14', '15-30', '31-60', '60+']
    df['recency_band'] = pd.cut(df['days_since_last_purchase'], bins=bins, labels=labels)
    # Discount label
    df['discount_label'] = df['discount_applied'].map({True: 'Discount', False: 'No Discount'})
    # Purchase date: current date minus days_since_last_purchase
    today = datetime.now().date()
    df['purchase_date'] = df['days_since_last_purchase'].apply(lambda x: today - timedelta(days=int(x)))
    # Write cleaned data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


def main() -> None:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(root, 'data', 'raw', 'ecommerce_customer_behavior.csv')
    output_path = os.path.join(root, 'data', 'processed', 'customers_clean.csv')
    df = ingest_and_clean(input_path, output_path)
    print(f"Cleaned data saved to {output_path} with {len(df)} records.")


if __name__ == '__main__':
    main()