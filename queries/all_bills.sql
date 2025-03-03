WITH bill_details AS (
  SELECT 
    b.bill_id,
    b.bill_number,
    b.title,
    b.description,
    CASE 
      WHEN b.bill_number LIKE 'H%' THEN 'House'
      WHEN b.bill_number LIKE 'S%' THEN 'Senate'
      ELSE 'Other'
    END as chamber,
    b.status_date,
    h.date AS last_action_date,
    h.action AS last_action,
    -- Calculate progress percentage based on status
    CASE 
      WHEN b.status = 1 THEN 25  -- Introduced
      WHEN b.status = 2 THEN 50  -- In committee
      WHEN b.status = 3 THEN 75  -- Passed committee
      WHEN b.status = 4 THEN 90  -- Passed chamber
      WHEN b.status = 5 THEN 100 -- Enacted
      ELSE 0
    END AS progress_percentage,
    -- Create status_field in the format shown in example
    'Status: ' || 
    CASE 
      WHEN b.status = 1 THEN 'Introduced'
      WHEN b.status = 2 THEN 'In Committee'
      WHEN b.status = 3 THEN 'Passed Committee'
      WHEN b.status = 4 THEN 'Passed Chamber'
      WHEN b.status = 5 THEN 'Enacted'
      ELSE 'Unknown'
    END || 
    ' on ' || b.status_date || ' - ' || 
    CASE 
      WHEN b.status = 1 THEN 25  -- Introduced
      WHEN b.status = 2 THEN 50  -- In committee
      WHEN b.status = 3 THEN 75  -- Passed committee
      WHEN b.status = 4 THEN 90  -- Passed chamber
      WHEN b.status = 5 THEN 100 -- Enacted
      ELSE 0
    END || '% progression' as status_field,
    'https://legiscan.com/TX/bill/' || b.bill_number || '/2025' as url,
    t.state_link as bill_text_link
  FROM legiscan.bills b
  -- Join with history to get the latest action
  JOIN (
    SELECT 
      bill_id,
      date,
      action,
      ROW_NUMBER() OVER (PARTITION BY bill_id ORDER BY date DESC) as rn
    FROM 
      legiscan.bill_history
  ) h ON b.bill_id = h.bill_id AND h.rn = 1
  -- Join with texts to get the latest text link
  JOIN (
    SELECT 
      _dlt_root_id,
      type,
      state_link,
      ROW_NUMBER() OVER (PARTITION BY _dlt_root_id ORDER BY date DESC) as rn
    FROM 
      legiscan.bills_texts
  ) t ON b._dlt_id = t._dlt_root_id AND t.rn = 1
),
texas_impact_bills AS (
  SELECT * FROM texas_impact.bills
)

SELECT
  bd.*,
  tib.Position,
  tib.Topic,
  tib.Description as texas_impact_description  
FROM bill_details bd
JOIN texas_impact_bills tib ON bd.bill_number = tib.bill_number 