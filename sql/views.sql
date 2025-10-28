-- Example views built on the customers table

-- Summarise customer counts and average metrics by recency band
CREATE VIEW IF NOT EXISTS recency_summary AS
SELECT recency_band,
       COUNT(*)               AS customers,
       AVG(total_spend)       AS avg_spend,
       AVG(avg_rating)        AS avg_rating
FROM customers
GROUP BY recency_band
ORDER BY MIN(days_since_last_purchase);

-- Identify the top membership tier (by revenue) in each city
CREATE VIEW IF NOT EXISTS top_tier_by_city AS
WITH city_tier AS (
  SELECT city,
         membership_type,
         SUM(total_spend) AS revenue,
         RANK() OVER (PARTITION BY city ORDER BY SUM(total_spend) DESC) AS rnk
  FROM customers
  GROUP BY city, membership_type
)
SELECT city, membership_type, revenue
FROM city_tier
WHERE rnk = 1;