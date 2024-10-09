---
queries:
   - state: state.sql
---

# {params.state_name}

```bills
select
   date_trunc('month', last_action_date) as month,
   count(DISTINCT bill_id) as total_bills
from bills
where state = '${params.state_name}'
group by month
order by month desc
```

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

<LineChart
   data={bills}
   x=month
   y=total_bills
   title="Period Care Bills"
   subtitle="12 Month Rolling Total"
/>


<DataTable data={all_bills} rows=all>
<Column id=date/>
<Column id=bill_number/>
<Column id=title/>
<Column id=last_action/>
<Column id=text_url/>
</DataTable>


