-- First level: Position → Chamber
SELECT 
  Position as source,
  chamber as target,
  COUNT(*) as value
FROM ${all_bills}
GROUP BY Position, chamber

UNION ALL

-- Second level: Chamber → Topic
SELECT 
  chamber as source,
  Topic as target,
  COUNT(*) as value
FROM ${all_bills}
GROUP BY chamber, Topic 