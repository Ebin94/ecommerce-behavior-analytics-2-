# Methodology

This project follows a simple yet complete analytics pipeline from raw data to visualisations and models.  The steps are modular so that you can run only what you need or extend the workflow with your own scripts.

## Data Flow

Below is a high‑level representation of the data flow through the repository.  Each arrow indicates a process implemented in a Python script or notebook.

```
  [Raw CSV]
      │  (src/01_ingest_clean.py)
      ▼
 [Clean CSV] ──┐
               │   (src/02_to_database.py)                 ┌──────────────┐
               ├──► [Database: customers table] ─────────► │   SQL queries │
               │                                          └──────────────┘
               │   (src/03_export_for_tableau.py)
               └──► [Tableau export] → (visualised manually)

  [Clean CSV] → (notebooks/01_eda.ipynb) → EDA and insights
  [Clean CSV] → (notebooks/02_feature_engineering.ipynb) → feature matrices
  [Features]  → (notebooks/03_model_satisfaction_or_value.ipynb) → models and evaluation
```

### Step 1 – Ingestion & Cleaning

`src/01_ingest_clean.py` reads the raw CSV from `data/raw/` and performs the following transformations:

- **Type enforcement:** ensures age and items are integers, spend and rating are floats, and the discount indicator is boolean.
- **Title‑casing:** standardises string fields to title case so that values are consistent.
- **Missing values:** fills missing satisfaction with `"Unknown"`.
- **Derived fields:** flags high‑value customers (`total_spend` ≥ 1000), computes recency bands from days since last purchase, creates a human‑readable discount label and calculates the purchase date from the current date.

The cleaned dataset is saved to `data/processed/customers_clean.csv`.

### Step 2 – Database & SQL

`src/02_to_database.py` reads the cleaned CSV and writes it to a relational database (SQLite by default, PostgreSQL if `DATABASE_URL` is provided).  The table schema is defined in `sql/schema.sql`.  Once loaded, you can execute SQL queries from `sql/analysis_queries.sql` or build your own.  Example views are defined in `sql/views.sql` to summarise recency and identify top membership tiers by city.

### Step 3 – Exploratory Analysis

The `notebooks/01_eda.ipynb` notebook explores the cleaned data: it computes summary statistics, plots distributions and relationships (e.g., spending by tier, satisfaction vs recency) and annotates insights inline.  Charts are created with Matplotlib for reproducibility.

### Step 4 – Feature Engineering

`notebooks/02_feature_engineering.ipynb` prepares data for modelling.  It encodes categorical variables (ordinal encoding for membership type and one‑hot encoding for city and gender), derives binary targets (high‑value vs others or satisfied vs others) and splits the data into training and testing sets.  Intermediate feature files are saved to `data/interim/` for reuse.

### Step 5 – Modelling

`notebooks/03_model_satisfaction_or_value.ipynb` trains two classifiers – logistic regression and XGBoost – on the engineered features.  It reports accuracy, ROC–AUC and confusion matrices and plots feature importances.  The notebook discusses which features are most predictive and cautions against overfitting given the small dataset size.
