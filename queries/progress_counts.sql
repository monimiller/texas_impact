SELECT progress_percentage, COUNT(*) as count
FROM ${all_bills}
GROUP BY progress_percentage
ORDER BY progress_percentage