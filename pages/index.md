---
title: Texas Impact Reproductive Issues Bill Tracker
queries:
  - bills: all_bills.sql
---

[Join the Reproductive Issues Champions!](https://secure.everyaction.com/ijP2C35RDk-5hJVeXth1Fw2)

## House Bills We Support

<DataTable 
  data={bills.where(`chamber = 'House' and position = 'Support'`)} 
  search=true 
  groupBy=Topic 
  sort="status_date desc"
>
  <Column id=url contentType=link linkLabel=bill_number title="Bill Number" opposite=Position openInNewTab=true/>
  <!-- TODO <Column id=last_action_date /> -->
  <!-- TODO <Column id=last_action /> -->
  <Column id=Position />
  <Column id=texas_impact_description	title="Description" />
</DataTable>

## House Bills We Oppose

<DataTable 
  data={bills.where(`chamber = 'House' and position = 'Oppose'`)}
  search=true 
  groupBy=Topic 
  sort="status_date desc"
>
  <Column id=url contentType=link linkLabel=bill_number title="Bill Number" opposite=Position openInNewTab=true/>
  <!-- TODO <Column id=last_action_date /> -->
  <!-- TODO <Column id=last_action /> -->
  <Column id=Position />
  <Column id=texas_impact_description	title="Description" />
</DataTable>

## Senate Bills We Support

<DataTable 
  data={bills.where(`chamber = 'Senate' and position = 'Support'`)}
  search=true 
  groupBy=Topic 
  sort="status_date desc"
>
  <Column id=url contentType=link linkLabel=bill_number title="Bill Number" opposite=Position openInNewTab=true/>
  <Column id=last_action_date />
  <Column id=last_action />
  <Column id=Position />
  <Column id=texas_impact_description	title="Description" />
</DataTable>

## Senate Bills We Oppose

<DataTable 
  data={bills.where(`chamber = 'Senate' and position = 'Oppose'`)}
  search=true 
  groupBy=Topic 
  sort="status_date desc"
>
  <Column id=url contentType=link linkLabel=bill_number title="Bill Number" opposite=Position openInNewTab=true/>
  <Column id=last_action_date />
  <Column id=last_action />
  <Column id=Position />
  <Column id=texas_impact_description	title="Description" />
</DataTable>
