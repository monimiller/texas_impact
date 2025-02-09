SELECT 

    l.number,
    t.topic,
    t.position,
    t.description as texas_impact_description,
    l.url,
    l.status_date,
    l.status,
    l.last_action_date,
    l.last_action,
    l.title
from legiscan.monitored_bills l
LEFT JOIN texas_impact.bills t ON l.number = t.bill_number;
