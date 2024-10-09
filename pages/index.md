---
title: Period Care Bills Tracker
queries:
   - bills_monthly: bills_monthly.sql
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

<!-- FIXME Not over time -->
<LineChart
  data={bills_monthly}
  x=last_action_date
  y=rolling_total_bills
  title="Bills in the United States"
  subtitle="12 Month Rolling Total"
  colorPalette={['#8789fe']}
/>


```bills_by_state
select
state as state_name,
'/state/' || state as state_link,
count(DISTINCT bill_id) as total_bills
from bills
group by state
```

<USMap
  data={bills_by_state}
  state=state_name
  abbreviations=true
  value=total_bills
  link=state_link
  title="Period Care Bills by State"
  colorPalette={['white', '#8789fe']}
/>
