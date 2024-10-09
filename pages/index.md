---
title: Period Care Bills Tracker
---

The United States is going through a overhaul of period care access 

```bills_most_recent
select
  strptime(concat(Month, ' ', Year::int), '%B %Y') as date,
  trim(regexp_replace(Indicator, '\\(.*?\\)', '')) as indicator_trimmed,
  -- window function division of next row
  "Data Value" / lead("Data Value") over (order by date) as pct_of_deaths,
  "Data Value" as total_deaths
from deaths
where "State Name" = 'United States'
and indicator_trimmed in ('Number of Drug Overdose Deaths', 'Number of Deaths')
order by date desc
limit 2
```



```bills_monthly
select
  "State Name",
  strptime(concat(Month, ' ', Year::int), '%B %Y') as date,
  trim(regexp_replace(Indicator, '\\(.*?\\)', '')) as indicator_trimmed,
  case
    when indicator_trimmed = 'Number of Drug Overdose Deaths' then 'All Drugs'
    else indicator_trimmed
  end as indicator_clean,
  "Data Value" as total_deaths
from deaths
where "State Name" = 'United States'
and indicator_clean = '${inputs.indicator.value}'
order by date desc
```

```sql bills_by_state
 select
   state,
   '/state/' || state as link,
   state,
   sum(bill_id) as total_bills
 from bills
 where state not in ('United States', 'Alaska', 'Hawaii')
  -- and extract(year from last_action_date) = 2024
  -- and extract(month from last_action_date) = 4
 group by all
 order by total_bills desc
```

<LineChart
  data={bills_monthly}
  x=date
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