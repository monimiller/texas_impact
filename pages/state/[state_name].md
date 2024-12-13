---
queries:
   - state: state.sql
---

# {params.state_name}

```bills
SELECT
   date_trunc('month', last_action_date) AS month,
   COUNT(DISTINCT bill_number) AS total_bills,
   SUM(COUNT(DISTINCT bill_number)) OVER (ORDER BY date_trunc('month', last_action_date) ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS rolling_total_bills
FROM bills
WHERE state = '${params.state_name}'
GROUP BY date_trunc('month', last_action_date)
ORDER BY month DESC;
```

<AreaChart
   data={bills}
   x=month
   y=rolling_total_bills
   title="Period Care Bills"
   subtitle="12 Month Rolling Total"
/>

```get_state_summary
select
  state as state_name,
  summary,
  analysis,
  zoomer_vibe,
from generated.state_period_care_vibes
where state = '${params.state_name}'
```

<Details title="Summary">

<Value 
   data={get_state_summary}
   column=summary
/>   

</Details>

<Details title="Analysis">

<Value 
   data={get_state_summary}
   column=analysis
/>   

</Details>

<Details title="Vibes">

<Value 
   data={get_state_summary}
   column=zoomer_vibe
/>   

</Details>

```all_bills
select
  state,
  last_action_date as date,
  bill_number,
  bill_id,
  text_url,
  last_action,
  title
from bills
where state = '${params.state_name}'
order by date desc
```

<DataTable data={all_bills} rows=all search=true rowShading=true rowLines=false>
  <Column id=date fmt="yyyy-mm-dd" title="Date" />
  <Column id=text_url contentType=link linkLabel=bill_number title="Bill Number" wrapTitle=true />
  <Column id=title wrap=true title="Title" />
  <Column id=last_action title="Last Action" wrap=true />
</DataTable>

<LastRefreshed prefix="Data last updated"/>