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

```sql bills_by_state
 select
   state,
   '/state/' || state as link,
   state,
   count(DISTINCT bill_id) as total_bills
 from bills
 where state not in ('United States', 'Alaska', 'Hawaii')
  -- and extract(year from last_action_date) = 2024
  -- and extract(month from last_action_date) = 4
 group by all
 order by total_bills desc
```

<!-- FIXME Not over time -->
<LineChart
  data={bills_monthly}
  x=month
  y=total_bills
  title="Bills in the United States"
  subtitle="12 Month Rolling Total"
/>
<AreaMap
  data={bills_by_state}
  geoJsonUrl='https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_1_states_provinces.geojson'
  geoId=postal
  areaCol=state
  value=total_bills
  link=link
  title="Period Care Bills by State"
  height=200
/>