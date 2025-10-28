# E‑Commerce Behavior Analytics

This repository contains a complete, end‑to‑end analytics workflow for an e‑commerce customer behaviour dataset.  The project demonstrates how to ingest and clean data with Python, design a relational schema and run advanced SQL analysis, perform exploratory data analysis and build simple predictive models in Jupyter notebooks, and export a tidy dataset ready for Tableau visualisations.

## Overview

**Goal:** analyse customer behaviour, spending and satisfaction patterns for an online store.  The workflow is organised into Python scripts, SQL files and notebooks that can be run end‑to‑end or independently.  Key findings from the current dataset include:

* **Gold vs Bronze spending:** gold members spend roughly 2–3× more than bronze members (average spend ≈ £1 311 vs £473)【31064417504200†screenshot】.
* **Discounts attract low spenders:** customers who received a discount spent less on average (~£787) than those without a discount (~£903)【31064417504200†screenshot】.
* **Satisfied customers repurchase sooner:** satisfied customers have the shortest average time since last purchase (~18 days) whereas unsatisfied customers wait much longer (~43 days)【31064417504200†screenshot】.

The repository structure, scripts and notebooks are documented below.

## Project Structure

```
ecommerce‑behavior‑analytics/
├─ README.md                  # project overview (this file)
├─ data/
│  ├─ raw/
│  │  └─ ecommerce_customer_behavior.csv  # unmodified source data
│  ├─ interim/                # intermediate files (feature sets, etc.)
│  └─ processed/
│     ├─ customers_clean.csv  # cleaned dataset with derived fields
│     └─ customers_tableau.csv # final export for Tableau visualisation
├─ sql/
│  ├─ schema.sql              # table definitions
│  ├─ seed.sql                # optional seed data
│  ├─ views.sql               # optional views
│  └─ analysis_queries.sql    # example analytical queries
├─ notebooks/
│  ├─ 01_eda.ipynb            # exploratory data analysis
│  ├─ 02_feature_engineering.ipynb # prepare features and targets
│  └─ 03_model_satisfaction_or_value.ipynb # modelling notebook
├─ src/
│  ├─ 01_ingest_clean.py      # Python ETL: load, clean and enrich data
│  ├─ 02_to_database.py       # load cleaned data into a relational database
│  ├─ 03_export_for_tableau.py # extract final dataset for Tableau
│  └─ utils.py                # utility functions
├─ docs/
│  ├─ data_dictionary.md      # definitions of fields and derived attributes
│  ├─ methodology.md          # description of the pipeline and diagram
│  └─ challenges.md           # key considerations and limitations
├─ env/
│  └─ requirements.txt        # Python dependencies
├─ LICENSE                    # licence (MIT)
└─ .gitignore                 # ignore compiled files and local database
```

## Pipeline Summary

1. **Data ingestion and cleaning (Python)** – `src/01_ingest_clean.py` reads the raw CSV, enforces appropriate data types, applies title‑casing to string fields, fills missing satisfaction levels with *“Unknown”*, derives new fields (high‑value flag, recency bands, discount labels, purchase dates) and saves the result to `data/processed/customers_clean.csv`.
2. **Database setup and advanced SQL analysis** – `src/02_to_database.py` creates the `customers` table using `sql/schema.sql` and loads the cleaned CSV into a SQLite or PostgreSQL database via SQLAlchemy.  `sql/analysis_queries.sql` contains examples of window functions, percentiles and other analytical queries to run against the table.
3. **Exploratory data analysis and modelling (Python)** – Jupyter notebooks in `notebooks/` explore the cleaned data, visualise distributions and relationships, engineer features and train simple models (logistic regression and XGBoost).  The notebooks are self‑documenting, with markdown commentary explaining the code and insights.
4. **Tableau‑ready export** – `src/03_export_for_tableau.py` queries the final dataset from the database and writes `data/processed/customers_tableau.csv` containing only the fields needed for visualisation.

## How to Run

1. Install dependencies (Python 3.8+ required):

   ```bash
   pip install -r env/requirements.txt
   ```

2. Run the ETL pipeline to produce the cleaned data:

   ```bash
   python src/01_ingest_clean.py
   ```

3. Load the cleaned data into a database (SQLite by default, or set `DATABASE_URL` for PostgreSQL):

   ```bash
   python src/02_to_database.py
   ```

4. Execute SQL analytics by connecting to the database and running queries from `sql/analysis_queries.sql` (for example, using `psql` or any SQL client).  Example outputs are documented in the `docs/` folder.

5. Open the exploratory notebooks:

   ```bash
   jupyter notebook notebooks/01_eda.ipynb
   ```

   Follow the notebooks in order for feature engineering and modelling.

6. Export the final dataset for Tableau:

   ```bash
   python src/03_export_for_tableau.py
   ```

## SQL Showcase

Here are two illustrative queries defined in `sql/analysis_queries.sql`.  They show how window functions and percentiles can be used to derive insights from the `customers` table:

* **Top membership tier by city** – rank membership types within each city by total revenue and return only the top tier per city.

  ```sql
  WITH city_tier AS (
    SELECT city, membership_type,
           SUM(total_spend) AS revenue,
           RANK() OVER (PARTITION BY city ORDER BY SUM(total_spend) DESC) AS rnk
    FROM customers
    GROUP BY city, membership_type
  )
  SELECT *
  FROM city_tier
  WHERE rnk = 1;
  ```

* **Revenue percentiles** – compute the median (p50) and 90th percentile (p90) of total spending:

  ```sql
  SELECT
    percentile_cont(0.5) WITHIN GROUP (ORDER BY total_spend) AS p50,
    percentile_cont(0.9) WITHIN GROUP (ORDER BY total_spend) AS p90
  FROM customers;
  ```

## Limitations

This project is intended as a portfolio exercise.  The dataset contains only 350 observations, so results may not generalise and models can easily overfit.  The `purchase_date` field is inferred from *Days Since Last Purchase*, which introduces synthetic dates.  Correlation does not imply causation – discounts may coincide with low spending rather than cause it.  Feel free to adapt the scripts for larger or real‑world datasets.
