WITH base_bills AS (
    SELECT
        l.bill_number,
        t.topic,
        t.position,
        t.description as texas_impact_description,
        l.url,
        l.status_date,
        l.status,
        -- TODO l.last_action as last_action_date,
        -- TODO l.last_action_desc as last_action,
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
