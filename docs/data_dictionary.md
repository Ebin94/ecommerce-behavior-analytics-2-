# Data Dictionary

This dictionary describes the fields present in the cleaned dataset (`customers_clean.csv`).  Types refer to how values are stored in the database and Python.  Derived columns are computed during the ETL process.

| Field | Type | Description |
| --- | --- | --- |
| `customer_id` | int | Unique identifier for each customer |
| `gender` | string | Customer gender (e.g., *Female*, *Male*) |
| `age` | int | Age in years |
| `city` | string | City where the customer is based |
| `membership_type` | string | Loyalty tier (*Bronze*, *Silver*, *Gold*) |
| `total_spend` | float | Lifetime spending by the customer (£) |
| `items_purchased` | int | Number of items purchased overall |
| `avg_rating` | float | Average product rating given by the customer (1–5) |
| `discount_applied` | boolean | Whether the last purchase involved a discount |
| `days_since_last_purchase` | int | Days between today and the most recent purchase |
| `satisfaction_level` | string | Self‑reported satisfaction (*Satisfied*, *Neutral*, *Unsatisfied*, *Unknown*) |
| `purchase_date` | date | Derived: date of the most recent purchase (today minus `days_since_last_purchase`) |
| `is_high_value` | boolean | Derived: `true` if `total_spend` ≥ 1000 |
| `recency_band` | string | Derived: categorical band of recency (*0–14*, *15–30*, *31–60*, *60+*) |
| `discount_label` | string | Derived: *Discount* if `discount_applied` is `true`, else *No Discount* |
