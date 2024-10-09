---
title: Period Care Bills Tracker
---

The United States is going through a overhaul of period care access 

```bills_most_recent
    select
      last_action_date as date,
      -- Render something here
      -- bill_id / lead(bill_id) over (order by date) as pct_of_bills,
      -- bill_id as total_bills
    from bills
    -- where state = 'United States'
    order by date desc
    limit 2
```



```bills_monthly
select
  date_trunc('month', last_action_date) as month,
  count(DISTINCT bill_id) as total_bills
from bills
group by month
order by month desc
```

```bills_by_state
select
state as state_name,
'/state/' || state as state_link,
count(DISTINCT bill_id) as total_bills
from bills
group by state
```

<!-- FIXME Not over time -->
<LineChart
  data={bills_monthly}
  x=month
  y=total_bills
  title="Bills in the United States"
  subtitle="12 Month Rolling Total"
/>
<USMap
  data={bills_by_state}
  state=state_name
  abbreviations=true
  value=total_bills
  link=state_link
  title="Period Care Bills by State"
/>
