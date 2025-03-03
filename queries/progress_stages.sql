-- Convert the progress counts into a format for the funnel chart
WITH progress_labels AS (
  SELECT 
    progress_percentage,
    COUNT(*) as count,
    CASE 
      WHEN progress_percentage = 0 THEN 'Not Started'
      WHEN progress_percentage = 0.25 THEN 'Introduced'
      WHEN progress_percentage = 0.5 THEN 'In Committee'
      WHEN progress_percentage = 0.75 THEN 'Passed Committee'
      WHEN progress_percentage = 0.9 THEN 'Passed Chamber'
      WHEN progress_percentage = 1.0 THEN 'Enacted'
      ELSE 'Unknown'
    END as stage
  FROM ${all_bills}
  GROUP BY progress_percentage
)

SELECT 
  stage, 
  count
FROM progress_labels
ORDER BY 
  CASE 
    WHEN progress_percentage = 0 THEN 1
    WHEN progress_percentage = 0.25 THEN 2
    WHEN progress_percentage = 0.5 THEN 3
    WHEN progress_percentage = 0.75 THEN 4
    WHEN progress_percentage = 0.9 THEN 5
    WHEN progress_percentage = 1.0 THEN 6
    ELSE 7
  END 