---
title: Overdose Deaths in the United States
---

The United States is in the midst of an opioid epidemic: <Value data={deaths_most_recent} column="total_deaths" fmt=num0/> people died from drug overdoses in the last 12 months. That's <Value data={deaths_most_recent} column="pct_of_deaths" fmt=pct1/> of all deaths in the United States.



The CDC tracks the number of drug overdose deaths in the United States, and [breaks down the data by type of drug](https://data.cdc.gov/NCHS/VSRR-Provisional-Drug-Overdose-Death-Counts/xkb8-kh2a).


```indicators
select 
  trim(regexp_replace(Indicator, '\\(.*?\\)', '')) as indicator_trimmed,
  case
    when indicator_trimmed = 'Number of Drug Overdose Deaths' then 'All Drugs'
    else indicator_trimmed
  end as indicator_clean,
  sum("Data Value") as total_deaths
from cdc.deaths
where indicator_clean not in ('Number of Deaths', 'Percent with drugs specified')
group by all
order by total_deaths desc
```

```deaths_most_recent
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



```deaths_monthly
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

```sql deaths_by_state
select
  "State Name",
  '/state/' || "State Name" as link,
  state,
  trim(regexp_replace(Indicator, '\\(.*?\\)', '')) as indicator_trimmed,
  case
    when indicator_trimmed = 'Number of Drug Overdose Deaths' then 'All Drugs'
    else indicator_trimmed
  end as indicator_clean,
  sum("Data Value") as total_deaths
from deaths
where "State Name" not in ('United States', 'Alaska', 'Hawaii')
and indicator_clean = '${inputs.indicator.value}'
and Year = 2024
and Month = 'April'
group by all
order by total_deaths desc
```


<Dropdown 
  data={indicators} 
  name=indicator 
  value=indicator_clean 
  title=Indicator 
  defaultValue="All Drugs"
  order="total_deaths desc"
/>

<Grid cols=2>
  <LineChart
    data={deaths_monthly}
    x=date
    y=total_deaths
    title="{inputs.indicator.value} Deaths in the United States"
    subtitle="12 Month Rolling Total"
  />
  <AreaMap
    data={deaths_by_state}
    geoJsonUrl='https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_1_states_provinces.geojson'
    geoId=postal
    areaCol=State
    value=total_deaths
    link=link
    title="Drug Overdose Deaths by State"
    height=200
  />
</Grid>