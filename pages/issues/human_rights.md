---
title: Human Rights
description: Human rights are rights we have merely because we exist as human beings. They are inherent to all people, regardless of nationality, sex, national or ethnic origin, color, religion, language, or any other status. The Universal Declaration of Human Rights, which the United Nations General Assembly adopted in 1948, establishes a modern framework for linking public policy and law to the theological and moral tenets shared across the world’s faith traditions. 
queries:
  - all_bills: all_bills.sql
---

<DataTable 
  data={all_bills.where(`Topic = 'Human Rights'`)} 
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
