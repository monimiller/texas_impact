---
title: Texas Impact Reproductive Issues Bill Tracker
queries:
  - bills.sql
---

[Join the Reproductive Issues Champions!](https://secure.everyaction.com/ijP2C35RDk-5hJVeXth1Fw2)

<DataTable data={bills} search=true groupBy=Topic sort="last_action_date desc">
  <!-- TODO We could link to Texas Gov page  -->
	<Column id=url contentType=link linkLabel=number title="Bill Number" opposite=Position openInNewTab=true/>
  <Column id=last_action_date />
  <Column id=last_action />
  <!-- TODO Fix status to oppose support -->
  <Column id=Position />
  <Column id=texas_impact_description	title="Description" />
</DataTable>
