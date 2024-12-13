SELECT
  date_trunc('month', last_action_date) AS month,
  COUNT(DISTINCT bill_number) AS total_bills,
  SUM(COUNT(DISTINCT bill_number)) OVER (
    ORDER BY date_trunc('month', last_action_date) 
    ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
  ) AS rolling_total_bills
FROM legiscan.bills
WHERE 
  last_action_date >= CURRENT_DATE - INTERVAL '5 years'
  AND last_action_date <= CURRENT_DATE
GROUP BY date_trunc('month', last_action_date)
ORDER BY month;
