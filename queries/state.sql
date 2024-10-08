select 
    state as state_name,
    count(*) as bills
from legiscan.bills
where state not in ('United States', 'New York City')
  and extract(year from last_action_date) = 2024
  and extract(month from last_action_date) = 4
group by state
order by state_name