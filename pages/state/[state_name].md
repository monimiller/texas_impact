---
queries:
   - state: state.sql
---

# {params.state_name}

```bills
select
  state,
  last_action_date as date,
  bill_id as total_bills
from bills
where state = '${params.state_name}'
order by date desc
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
   x=date
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


