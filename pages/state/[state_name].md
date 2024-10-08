---
queries:
   - state: state.sql
---

# {params.state_name}


```deaths
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
where "State Name" = '${params.state_name}'
and indicator_trimmed in ('Number of Drug Overdose Deaths')
order by date desc
```

<LineChart
   data={deaths}
   x=date
   y=total_deaths
   title="Drug Overdose Deaths"
   subtitle="12 Month Rolling Total"
/>

```sql indicator
select
  trim(regexp_replace(Indicator, '\\(.*?\\)', '')) as indicator_trimmed,
  case
      when indicator_trimmed = 'Number of Drug Overdose Deaths' then 'All Drugs'
      else indicator_trimmed
   end as indicator_clean,
   sum("Data Value") as total_deaths
from deaths
where "State Name" = '${params.state_name}'
   and indicator_clean not in ('Percent with drugs specified')
   and Year = 2024
   and Month = 'April'
group by indicator_trimmed
order by total_deaths desc
```

## Deaths by Indicator - April 2024, Last 12 Months

<DataTable data={indicator} rows=all>
<Column id=indicator_clean/>
<Column id=total_deaths/>
</DataTable>


