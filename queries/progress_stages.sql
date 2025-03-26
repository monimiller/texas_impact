-- Convert the progress counts into a format for the funnel chart
WITH bill_stages AS (
  SELECT 
    CASE 
      WHEN last_action LIKE 'Filed%' THEN 'Filed'
      WHEN last_action LIKE 'Read first time%' THEN 'Read First Time'
      WHEN last_action LIKE 'Referred to%' THEN 'In Committee'
      WHEN last_action LIKE '%Committee report%' THEN 'Committee Reported'
      WHEN last_action LIKE '%passed%committee%' OR last_action LIKE '%Committee report%' THEN 'Passed Committee'
      WHEN last_action LIKE '%passed%' AND last_action NOT LIKE '%committee%' THEN 'Passed Chamber'
      WHEN last_action LIKE '%signed%governor%' OR last_action LIKE '%enacted%' OR last_action LIKE '%adopted%' THEN 'Enacted/Adopted'
      ELSE 'Other Actions'
    END as stage,
    COUNT(*) as count
  FROM ${all_bills}
  GROUP BY stage
),
stage_order AS (
  SELECT 
    stage,
    count,
    CASE 
      WHEN stage = 'Filed' THEN 1
      WHEN stage = 'Read First Time' THEN 2
      WHEN stage = 'In Committee' THEN 3
      WHEN stage = 'Committee Reported' THEN 4
      WHEN stage = 'Passed Committee' THEN 5
      WHEN stage = 'Passed Chamber' THEN 6
      WHEN stage = 'Enacted/Adopted' THEN 7
      ELSE 8
    END as display_order
  FROM bill_stages
)

SELECT 
  stage, 
  count
FROM stage_order
ORDER BY display_order 