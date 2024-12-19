WITH daily_counts AS (
  SELECT
    last_action_date::date AS day,
    COUNT(DISTINCT bill_id) as total_bills
  FROM legiscan.bills
  WHERE 
    last_action_date >= '${inputs.selected_timeframe.start}'
    AND last_action_date <= '${inputs.selected_timeframe.end}'
  GROUP BY last_action_date::date
)
SELECT
  day,
  total_bills,
  SUM(total_bills) OVER (
    ORDER BY day
  ) as rolling_total_bills
FROM daily_counts
ORDER BY day;
