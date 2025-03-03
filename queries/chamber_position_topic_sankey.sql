-- First level: Chamber → Position
SELECT 
  chamber as source,
  Position as target,
  COUNT(*) as value
FROM ${all_bills}
GROUP BY chamber, Position

UNION ALL

-- Second level: Position → Topic
SELECT 
  Position as source,
  Topic as target,
  COUNT(*) as value
FROM ${all_bills}
GROUP BY Position, Topic 