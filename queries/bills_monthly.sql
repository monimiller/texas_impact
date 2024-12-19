WITH all_time_totals AS (
  SELECT
    last_action_date::date AS day,
    COUNT(DISTINCT bill_id) as total_bills
  FROM legiscan.bills
  GROUP BY last_action_date::date
),
filtered_days AS (
  SELECT
    day,
    total_bills,
    SUM(total_bills) OVER (ORDER BY day) as rolling_total_bills
  FROM all_time_totals
)
SELECT
  day,
  total_bills,
  rolling_total_bills
FROM filtered_days
WHERE 
  day >= '${inputs.selected_timeframe.start}'
  AND day <= '${inputs.selected_timeframe.end}'
ORDER BY day;
