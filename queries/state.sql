select 
    state as state_name,
    COUNT(DISTINCT bill_number) AS total_bills,
from legiscan.bills
group by state
order by total_bills desc