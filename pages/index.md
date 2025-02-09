---
title: Texas Impact Bill Tracker
queries:
  - bills.sql
---

https://texasimpact.org

<DataTable data={bills} search=true groupBy=Topic sort="last_action_date desc">
  <!-- TODO We could link to Texas Gov page  -->
	<Column id=url contentType=link linkLabel=number title="Bill Number" opposite=Position openInNewTab=true/>
  <Column id=last_action_date />
  <Column id=last_action />
  <!-- TODO Fix status to oppose support -->
  <Column id=Position />
  <Column id=texas_impact_description	title="Description" />
</DataTable>
