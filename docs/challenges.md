# Challenges & Considerations

This project was developed as a learning exercise rather than a production system.  The following points outline some of the key challenges and limitations encountered.

* **Small sample size:** the dataset contains only 350 rows, making it easy for models to overfit.  High classification accuracy should be interpreted cautiously – it is likely driven by simple threshold rules (e.g., spending over £1 000 always classifies as high value).

* **Synthetic dates:** the `purchase_date` is inferred by subtracting *Days Since Last Purchase* from today.  In a real system you would store actual timestamps; here the assumption introduces artificial seasonality and precludes accurate time‑series analysis.

* **Correlation vs causation:** the data suggests that discounts are associated with lower spending, but this may reflect marketing strategy (discounts targeted at low spenders) rather than a causal effect.  Always combine data analysis with domain knowledge.

* **Biases and missing data:** satisfaction ratings may be self‑reported by a subset of customers, leading to potential bias.  Missing satisfaction values are filled with `Unknown`, which groups all types of non‑responses together.

* **Balancing simplicity vs realism:** this repository deliberately emphasises clarity and reproducibility over complexity.  For production use you would add error handling, parameterise file paths, support incremental loads and enforce database constraints.
