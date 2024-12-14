---
title: Period Care Bills Tracker
---

## **28 states** require free period products in various public restrooms

Are you compliant?

[Get Periodic!](https://www.getperiodic.org/periodicproducts)

```sql date_options
SELECT 
  last_action_date
FROM legiscan.bills
WHERE last_action_date >= '2009-01-01'
ORDER BY last_action_date DESC
```

<DateRange
    name=selected_timeframe
    data={date_options}
    dates=last_action_date
    defaultValue="Last 12 Months"
/>


```bills_monthly
SELECT
  date_trunc('month', last_action_date) AS month,
  COUNT(DISTINCT bill_number) AS total_bills,
  SUM(COUNT(DISTINCT bill_number)) OVER (
    ORDER BY date_trunc('month', last_action_date) 
    ROWS BETWEEN 11 PRECEDING AND CURRENT ROW
  ) AS rolling_total_bills
FROM legiscan.bills
WHERE 
  last_action_date >= '${inputs.selected_timeframe.start}'
  AND last_action_date <= '${inputs.selected_timeframe.end}'
GROUP BY date_trunc('month', last_action_date)
ORDER BY month
```

<AreaChart
data={bills_monthly}
x=month
y=rolling_total_bills
title="Bills in the United States"
subtitle="12 Month Rolling Total"
/>

```bills_by_state
select
state as state_name,
'/state/' || state as state_link,
count(DISTINCT bill_id) as total_bills
from bills
WHERE 
  last_action_date >= '${inputs.selected_timeframe.start}'
  AND last_action_date <= '${inputs.selected_timeframe.end}'
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