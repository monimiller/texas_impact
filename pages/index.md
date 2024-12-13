---
title: Period Care Bills Tracker
queries:
  - bills_monthly: bills_monthly.sql
---

## **28 states** require free period products in various public restrooms

Are you compliant?

[Get Periodic!](https://www.getperiodic.org/periodicproducts)

<AreaChart
  data={bills_monthly}
  x=month
  y=rolling_total_bills
  title="Bills in the United States"
  subtitle="Rolling Total"
/>

```bills_by_state
select
state as state_name,
'/state/' || state as state_link,
count(DISTINCT bill_id) as total_bills
from bills
group by state
```

<!-- BUG: https://github.com/evidence-dev/evidence/issues/2908 -->
<USMap
  data={bills_by_state}
  state=state_name
  abbreviations=true
  value=total_bills
  link=state_link
  title="Period Care Bills by State"
  colorScale=default
/>

<LastRefreshed prefix="Data last updated"/>