---
title: Bill Details
queries:
  - single_bill: bill_detail.sql
  - all_bills: all_bills.sql
  # TODO: add authors
---


# {params.bill_number}: <Value data={single_bill} column="title" />

<Grid columnsWide={3}>
  <BigValue data={single_bill} value=chamber title="Chamber" />
  <!-- TODO backgroundColor={positionColor}  -->
  <BigValue data={single_bill} value=Position title="Position" textColor="white" />
  <BigValue data={single_bill} value=Topic title="Topic" />
</Grid>

<!-- ## Bill Progress -->

<!-- barColor={positionColor}  -->
<DataTable data={single_bill} showHeader={false}>
  <Column id="progress_percentage" 
          contentType="bar" 
          backgroundColor="#f5f5f5" 
          fmt="pct"
          title="Bill Progress" />
</DataTable>

<Grid columnsWide={3}>
  <BigValue data={single_bill} value=status_field title="Current Status" />
  <BigValue data={single_bill} value=last_action_date title="Last Action Date" />
  <BigValue data={single_bill} value=last_action title="Last Action" />
</Grid>

## Description

<Alert type="info">
  <Value data={single_bill} column="texas_impact_description" />
</Alert>

<!-- FIXME: links are not working -->
<!-- ## Links

<Grid columnsWide={3}>
  <LinkButton url={single_bill.url}>
    Full Bill
  </LinkButton>
  <LinkButton url={single_bill.bill_detail_url}>
    Bill Detail
  </LinkButton>
  <LinkButton url={single_bill.bill_text_link}>
    Bill Text
  </LinkButton>
</Grid> -->

<!-- FIXME: authors are not working -->
<!-- ## Authors

<DataTable 
  data={single_bill} 
>
  <Column id="authors" title="Authors" />
  <Column id="sponsors" title="Sponsors" />
  <Column id="coauthors" title="Coauthors" />
  <Column id="cosponsors" title="Cosponsors" />
</DataTable> -->

---

<LastRefreshed />  
