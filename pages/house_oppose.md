---
title: House Bills We Oppose
queries:
  - bills: all_bills.sql
---

[Join the Reproductive Issues Champions!](https://secure.everyaction.com/ijP2C35RDk-5hJVeXth1Fw2)

<DataTable 
  data={bills.where(`chamber = 'House' and position = 'Oppose'`)}
  search=true 
  groupBy=Topic 
  sort="status_date desc"
  link=bill_detail_url
>
  <Column id=bill_number title="Bill Number" opposite=Position />
  <Column id=status_field title="Status" />
  <Column id=progress_percentage title="Progress" contentType=bar barColor=#53768a backgroundColor=#f5f5f5 fmt=pct />
  <Column id=last_action_date title="Last Updated" />
  <Column id=last_action title="Action" />
  <Column id=bill_text_link contentType=link linkLabel="View Text" title="Bill Text" openInNewTab=true />
  <Column id=texas_impact_description	title="Description" class="description-column" />
</DataTable>
