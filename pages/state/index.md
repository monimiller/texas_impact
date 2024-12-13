---
title: State Leaderboard
queries:
    - state: state.sql
---

Click on a state to see more detail


```sql state_with_link
select *, '/state/' || state_name as link
from ${state}
order by total_bills desc
```

<DataTable data={state_with_link} link=link rows=all>
    <Column id=state_name />
    <Column id=total_bills contentType=colorscale colorScale=default />
</DataTable>

<LastRefreshed prefix="Data last updated"/>