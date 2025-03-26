---
title: Economic Justice
queries:
  - all_bills: all_bills.sql
---

<DataTable 
  data={all_bills.where(`Topic = 'Economic Justice'`)} 
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
