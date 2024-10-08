SELECT
  state,
  COUNT(*) AS bill_count,
  '/state/' || LOWER(state) AS link
FROM
  bills
GROUP BY
  state
ORDER BY
  state;