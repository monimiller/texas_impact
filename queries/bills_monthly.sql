SELECT
  last_action_date,
  COUNT(DISTINCT bill_number) AS total_bills_actions,
  SUM(COUNT(DISTINCT bill_number)) OVER (ORDER BY last_action_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS rolling_total_bills
FROM legiscan.bills
GROUP BY last_action_date
ORDER BY last_action_date;
