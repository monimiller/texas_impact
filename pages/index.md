---
title: Texas Impact Legislative Dashboard
queries:
  - all_bills: all_bills.sql
  - progress_counts: progress_counts.sql
  - topic_counts: topic_counts.sql
  - total_count: total_count.sql
  - house_count: house_count.sql
  - senate_count: senate_count.sql
  - support_count: support_count.sql
  - oppose_count: oppose_count.sql
---

<BigValue 
  data={total_count} 
  value="value" 
  title="Total Bills Tracked" 
  subtitle="across all chambers"
/>

<Grid columnsWide={2}>
  <BigValue 
    data={house_count} 
    value="value" 
    title="House Bills" 
  />
  <BigValue 
    data={senate_count} 
    value="value" 
    title="Senate Bills" 
  />
</Grid>

<Grid columnsWide={2}>
  <BigValue 
    data={support_count} 
    value="value"
    title="Bills We Support" 
  />
  <BigValue 
    data={oppose_count} 
    value="value"
    title="Bills We Oppose" 
  />
</Grid>

## Bill Progress Overview

<BarChart 
  data={progress_counts}
  x=progress_percentage
  y=count
  xAxisTitle="Progress Percentage"
  yAxisTitle="Count"
/>

## Bills by Topic

<BarChart
  data={topic_counts}
  x=Topic
  y=count
  title="Bills by Topic"
/>

## Recent Activity

<DataTable 
  data={all_bills.limit(5)} 
  search=true
  formatColumnTitles=true
  defaultSort="last_action_date"
  defaultSortDirection="desc"
>
  <Column id=url contentType=link linkLabel=bill_number title="Bill Number" openInNewTab=true/>
  <Column id=chamber title="Chamber" />
  <Column id=Position title="Position" />
  <Column id=Topic title="Topic" />
  <Column id=status_field title="Status" />
  <Column id=last_action_date title="Last Updated" />
  <Column id=last_action title="Last Action" />
</DataTable>

---

<small>Last updated: {new Date().toLocaleDateString()}</small>
