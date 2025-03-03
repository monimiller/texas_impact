SELECT Topic, COUNT(*) as count
FROM ${all_bills}
GROUP BY Topic
ORDER BY count DESC