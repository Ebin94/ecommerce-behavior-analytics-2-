#!/usr/bin/env python
"""
Load the cleaned customer data into a relational database.

This script reads `data/processed/customers_clean.csv`, creates the `customers`
table using SQL contained in `sql/schema.sql` and inserts all rows via
SQLAlchemy.  By default it uses a local SQLite database (ecommerce.db);
providing a `DATABASE_URL` environment variable will override this.
"""
import os
import pandas as pd
from sqlalchemy import text
from src.utils import get_engine


def main() -> None:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_csv = os.path.join(root, 'data', 'processed', 'customers_clean.csv')
    schema_sql_file = os.path.join(root, 'sql', 'schema.sql')
    # Read cleaned dataset; parse purchase_date as date
    df = pd.read_csv(input_csv, parse_dates=['purchase_date'])
    engine = get_engine()
    # Create the customers table
    with engine.begin() as conn:
        with open(schema_sql_file, 'r') as f:
            schema_sql = f.read()
            conn.execute(text(schema_sql))
        # Insert data
        df.to_sql('customers', con=conn, if_exists='append', index=False)
        # Count rows
        count = conn.execute(text('SELECT COUNT(*) FROM customers')).scalar()
    print(f"Loaded {count} records into the database.")


if __name__ == '__main__':
    main()