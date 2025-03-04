SELECT 
  Topic as topic_name, 
  COUNT(*) as bill_count,
  SUM(CASE WHEN progress_percentage = 1.00 THEN 0 ELSE 1 END) as active_bills,
  '/topic/' || Topic as topic_link
FROM ${all_bills}
GROUP BY topic_name
ORDER BY bill_count DESC