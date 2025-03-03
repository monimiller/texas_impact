WITH base_bills AS (
    SELECT
        l.bill_number,
        t.topic,
        t.position,
        t.description as texas_impact_description,
        l.url,
        l.status_date,
        l.status,
        -- Get the latest action date and description
        (SELECT h.date FROM legiscan_bills.bill_history h WHERE h.bill_id = l.bill_id ORDER BY h.date DESC LIMIT 1) as last_action_date,
        (SELECT h.action FROM legiscan_bills.bill_history h WHERE h.bill_id = l.bill_id ORDER BY h.date DESC LIMIT 1) as last_action,
        -- Get the status label based on progress events
        CASE
            WHEN l.status = 1 THEN 'Introduced'
            WHEN l.status = 2 THEN 'Engrossed'
            WHEN l.status = 3 THEN 'Enrolled'
            WHEN l.status = 4 THEN 'Passed'
            WHEN l.status = 5 THEN 'Vetoed'
            WHEN l.status = 6 THEN 'Failed'
            ELSE 'Unknown'
        END as status_label,
        -- Calculate progress percentage based on status
        CASE
            WHEN l.status = 1 THEN 25
            WHEN l.status = 2 THEN 50
            WHEN l.status = 3 THEN 75
            WHEN l.status = 4 THEN 100
            WHEN l.status = 5 THEN 0
            WHEN l.status = 6 THEN 0
            ELSE 0
        END as progress_percentage,
        -- Create formatted status field like "Status: Introduced on November 12 2024 - 25% progression"
        CASE
            WHEN l.status = 1 THEN 'Status: Introduced on ' || l.status_date || ' - 25% progression'
            WHEN l.status = 2 THEN 'Status: Engrossed on ' || l.status_date || ' - 50% progression'
            WHEN l.status = 3 THEN 'Status: Enrolled on ' || l.status_date || ' - 75% progression'
            WHEN l.status = 4 THEN 'Status: Passed on ' || l.status_date || ' - 100% progression'
            WHEN l.status = 5 THEN 'Status: Vetoed on ' || l.status_date
            WHEN l.status = 6 THEN 'Status: Failed on ' || l.status_date
            ELSE 'Status: Unknown'
        END as status_field,
        -- Get bill text link - use bill_id for the join
        (SELECT bt.state_link 
         FROM legiscan_bills.bills__texts bt 
         JOIN legiscan_bills.bills b ON b.bill_id = l.bill_id AND b._dlt_id = bt._dlt_parent_id 
         ORDER BY bt.date DESC 
         LIMIT 1) as bill_text_link,
        -- Get bill text type (Introduced, Amended, etc.)
        (SELECT bt.type 
         FROM legiscan_bills.bills__texts bt 
         JOIN legiscan_bills.bills b ON b.bill_id = l.bill_id AND b._dlt_id = bt._dlt_parent_id 
         ORDER BY bt.date DESC 
         LIMIT 1) as bill_text_type,
        l.title,
        CASE 
            WHEN REGEXP_MATCHES(TRIM(UPPER(l.bill_number)), '^HB[0-9]') THEN 'House'
            WHEN REGEXP_MATCHES(TRIM(UPPER(l.bill_number)), '^SB[0-9]') THEN 'Senate'
            ELSE 'Other'
        END as chamber
    from legiscan.bills l
    LEFT JOIN texas_impact.bills t ON l.bill_number = t.bill_number
)
SELECT * FROM base_bills;
