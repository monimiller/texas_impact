-- First level: Position → Topic
SELECT 
  Position as source,
  Topic as target,
  COUNT(*) as value
FROM ${all_bills}
GROUP BY Position, Topic

UNION ALL

-- Second level: Topic → Chamber
SELECT 
  Topic as source,
  chamber as target,
  COUNT(*) as value
FROM ${all_bills}
GROUP BY Topic, chamber 