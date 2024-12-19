WITH monthly_counts AS (
  SELECT
    date_trunc('month', last_action_date) AS month,
    COUNT(DISTINCT bill_id) as total_bills
  FROM legiscan.bills
  WHERE 
    last_action_date >= '${inputs.selected_timeframe.start}'
    AND last_action_date <= '${inputs.selected_timeframe.end}'
  GROUP BY date_trunc('month', last_action_date)
),
filled_months AS (
  SELECT 
    month,
    total_bills
  FROM monthly_counts
)
SELECT
  month,
  total_bills,
  SUM(total_bills) OVER (
    ORDER BY month
  ) as rolling_total_bills
FROM filled_months
ORDER BY month;
