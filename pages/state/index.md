---
title: State Level Data
queries:
   - state: state.sql
---

Click on a state to see more detail


```sql state_with_link
select *, '/state/' || state_name as link
from ${state}
```

<DataTable data={state_with_link} link=link rows=all/>