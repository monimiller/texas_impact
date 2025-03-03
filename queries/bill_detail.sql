SELECT *
FROM ${all_bills}
WHERE bill_number = '${params.bill_number}'
LIMIT 1
