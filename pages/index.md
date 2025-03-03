---
title: Texas Impact Legislative Dashboard
queries:
  - all_bills.sql
  - progress_counts.sql
  - topic_counts.sql
---

<BigValue 
  data={all_bills} 
  value={all_bills.length} 
  title="Total Bills Tracked" 
  subtitle="across all chambers"
/>

<Grid columnsWide={2}>
  <BigValue 
    data={all_bills.where(`chamber = 'House'`)} 
    value={all_bills.where(`chamber = 'House'`).length} 
    title="House Bills" 
  />
  <BigValue 
    data={all_bills.where(`chamber = 'Senate'`)} 
    value={all_bills.where(`chamber = 'Senate'`).length} 
    title="Senate Bills" 
  />
</Grid>

<Grid columnsWide={2}>
  <BigValue 
    data={all_bills.where(`position = 'Support'`)} 
    value={all_bills.where(`position = 'Support'`).length} 
    title="Bills We Support" 
  />
  <BigValue 
    data={all_bills.where(`position = 'Oppose'`)} 
    value={all_bills.where(`position = 'Oppose'`).length} 
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
