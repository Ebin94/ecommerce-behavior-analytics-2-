-- Example analytical queries for the customers table

-- Top membership tier by city (using window functions)
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

-- Revenue percentiles (median and 90th percentile)
SELECT
  percentile_cont(0.5) WITHIN GROUP (ORDER BY total_spend) AS p50,
  percentile_cont(0.9) WITHIN GROUP (ORDER BY total_spend) AS p90
FROM customers;

-- Recency vs spend and rating
SELECT recency_band,
       COUNT(*) AS customers,
       AVG(total_spend) AS avg_spend,
       AVG(avg_rating) AS avg_rating
FROM customers
GROUP BY recency_band
ORDER BY MIN(days_since_last_purchase);

-- Discount effect within each membership tier
SELECT membership_type, discount_applied,
       AVG(total_spend) AS avg_spend,
       AVG(avg_rating) AS avg_rating,
       AVG(AVG(total_spend)) OVER (PARTITION BY membership_type) AS tier_baseline
FROM customers
GROUP BY membership_type, discount_applied;

-- Rolling 30‑day revenue (requires purchase_date)
SELECT purchase_date,
       SUM(total_spend) OVER (
         ORDER BY purchase_date
         ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
       ) AS rolling_30d_revenue
FROM customers
ORDER BY purchase_date;