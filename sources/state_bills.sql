SELECT
  bill_number,
  title,
  url,
  last_action_date,
  last_action
FROM
  bills
WHERE
  state = UPPER('${params.state_name}')
ORDER BY
  last_action_date DESC;