---
queries:
   - state: state.sql
---

# {params.state_name}

```bills
SELECT
   date_trunc('month', last_action_date) AS month,
   COUNT(DISTINCT bill_id) AS total_bills,
   SUM(COUNT(DISTINCT bill_id)) OVER (ORDER BY date_trunc('month', last_action_date) ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS rolling_total_bills
FROM bills
WHERE state = '${params.state_name}'
GROUP BY date_trunc('month', last_action_date)
ORDER BY month DESC;
```

<LineChart
   data={bills}
   x=month
   y=rolling_total_bills
   title="Period Care Bills"
   subtitle="12 Month Rolling Total"
/>

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

<DataTable data={all_bills} rows=all>
<Column id=date/>
<Column id=bill_number/>
<Column id=title/>
<Column id=last_action/>
<Column id=text_url/>
</DataTable>


