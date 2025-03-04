---
title: Bills Related to 
# <Value data={topic_info} column="topic_name"/> 
---

# <Value data={topic_info} column="topic_name"/> Bills

```sql topic_info
select 
  topic_name, 
  count(*) as bill_count,
  sum(case when status = 'Active' then 1 else 0 end) as active_bills,
  sum(case when status = 'Inactive' then 1 else 0 end) as inactive_bills
from bills
where lower(topic_name) = lower(${topic_name})
group by 1
```

<Alert status="info">
  There are <Value data={topic_info} column="bill_count"/> bills related to <Value data={topic_info} column="topic_name"/>.
  <Value data={topic_info} column="active_bills"/> are active and <Value data={topic_info} column="inactive_bills"/> are inactive.
</Alert>

## Bill Summary

```sql bills_by_topic
select 
  bill_id,
  bill_name,
  description,
  status,
  introduced_date,
  last_action_date,
  sponsor_name,
  chamber
from bills
where lower(topic_name) = lower(${topic_name})
order by last_action_date desc
```

<DataTable 
  data={bills_by_topic} 
  link={{
    column: "bill_id",
    href: "/bill/[bill_id]",
    hrefColumn: "bill_id"
  }}
/>

## Status Breakdown

```sql status_breakdown
select 
  status,
  count(*) as bill_count
from bills
where lower(topic_name) = lower(${topic_name})
group by 1
```

<BarChart 
  data={status_breakdown} 
  x="status" 
  y="bill_count"
  title="Bills by Status"
/>

## Recent Activity

```sql recent_actions
select 
  bill_id,
  bill_name,
  action_description,
  action_date
from bill_actions
join bills using(bill_id)
where lower(topic_name) = lower(${topic_name})
order by action_date desc
limit 10
```

<DataTable data={recent_actions} title="Recent Actions on Bills"/>

## Chamber Distribution

```sql chamber_breakdown
select 
  chamber,
  count(*) as bill_count
from bills
where lower(topic_name) = lower(${topic_name})
group by 1
```

<!-- TODO -->

## Bill Timeline

```sql bill_timeline
select 
  date_trunc('month', introduced_date) as month,
  count(*) as bills_introduced
from bills
where lower(topic_name) = lower(${topic_name})
  and introduced_date is not null
group by 1
order by 1
```

<LineChart 
  data={bill_timeline} 
  x="month" 
  y="bills_introduced"
  title="Bills Introduced Over Time"
/>

## Top Bill Sponsors

```sql top_sponsors
select 
  sponsor_name,
  count(*) as bills_sponsored
from bills
where lower(topic_name) = lower(${topic_name})
  and sponsor_name is not null
group by 1
order by 2 desc
limit 5
```

<BarChart 
  data={top_sponsors} 
  x="sponsor_name" 
  y="bills_sponsored"
  title="Top Bill Sponsors"
/>
