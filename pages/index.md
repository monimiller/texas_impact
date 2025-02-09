---
title: Texas Impact Bill Tracker
queries:
  - bills.sql
---

https://texasimpact.org

<DataTable data={bills} search=true >
  <!-- TODO We could link to Texas Gov page  -->
	<Column id=url contentType=link linkLabel=number title="Bill Number" />
  <Column id=status_date />
  <Column id=last_action_date />
  <Column id=last_action />
  <!-- TODO Fix status to oppose support -->
  <Column id=status />
  <Column id=title />
</DataTable>
