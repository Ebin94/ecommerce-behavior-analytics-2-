#!/usr/bin/env python
"""
Export a simplified customer dataset from the database for Tableau.

This script connects to the database using the same connection mechanism as
`02_to_database.py`, selects relevant fields from the `customers` table and
writes them to `data/processed/customers_tableau.csv`.  The resulting CSV can
be imported directly into Tableau for visualisations.
"""
import os
import pandas as pd
from sqlalchemy import text
from src.utils import get_engine


def main() -> None:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(root, 'data', 'processed', 'customers_tableau.csv')
    engine = get_engine()
    query = text('''
        SELECT
            customer_id,
            city,
            gender,
            age,
            membership_type,
            total_spend,
            items_purchased,
            avg_rating,
            discount_applied,
            days_since_last_purchase,
            satisfaction_level,
            purchase_date,
            recency_band
        FROM customers
    ''')
    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Exported {len(df)} rows to {output_path}.")


if __name__ == '__main__':
    main()