-- Schema definition for the customers table

CREATE TABLE IF NOT EXISTS customers (
  customer_id            INTEGER PRIMARY KEY,
  gender                 TEXT,
  age                    INTEGER,
  city                   TEXT,
  membership_type        TEXT,
  total_spend            NUMERIC(10,2),
  items_purchased        INTEGER,
  avg_rating             NUMERIC(3,2),
  discount_applied       BOOLEAN,
  days_since_last_purchase INTEGER,
  satisfaction_level     TEXT,
  purchase_date          DATE,
  is_high_value          BOOLEAN,
  recency_band           TEXT,
  discount_label         TEXT
);