---
title: Bill Details
queries:
  - bill_detail: bill_detail.sql
  - all_bills: all_bills.sql
---

<script>
  const bill = bill_detail[0];
  
  // Format the progress percentage for display
  const progressFormatted = (bill.progress_percentage * 100).toFixed(1) + '%';
  
  // Define color based on position
  const positionColor = bill.position === 'Support' ? '#2E8B57' : '#CD5C5C';
  
  // Format dates for better display
  const formatDate = (dateStr) => {
    if (!dateStr) return 'N/A';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };
</script>

# {bill.bill_number}: {bill.bill_title}

<div style="display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap;">
  <div style="background-color: #f5f5f5; padding: 16px; border-radius: 8px; min-width: 200px;">
    <h3 style="margin-top: 0;">Chamber</h3>
    <p style="font-size: 1.2rem; font-weight: 500;">{bill.chamber}</p>
  </div>
  
  <div style="background-color: {positionColor}; color: white; padding: 16px; border-radius: 8px; min-width: 200px;">
    <h3 style="margin-top: 0;">Position</h3>
    <p style="font-size: 1.2rem; font-weight: 500;">{bill.position}</p>
  </div>
  
  <div style="background-color: #f5f5f5; padding: 16px; border-radius: 8px; min-width: 200px;">
    <h3 style="margin-top: 0;">Topic</h3>
    <p style="font-size: 1.2rem; font-weight: 500;">{bill.topic}</p>
  </div>
</div>

## Bill Progress

<div style="width: 100%; background-color: #f5f5f5; height: 30px; border-radius: 4px; margin: 16px 0;">
  <div style="width: {bill.progress_percentage * 100}%; height: 100%; background-color: {positionColor}; border-radius: 4px; display: flex; align-items: center; justify-content: center;">
    <span style="color: white; font-weight: 500;">{(bill.progress_percentage * 100).toFixed(1)}%</span>
  </div>
</div>

<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; margin: 24px 0;">
  <div style="border: 1px solid #e5e7eb; padding: 16px; border-radius: 8px;">
    <h3>Current Status</h3>
    <p>{bill.status_field}</p>
  </div>
  
  <div style="border: 1px solid #e5e7eb; padding: 16px; border-radius: 8px;">
    <h3>Last Action Date</h3>
    <p>{formatDate(bill.last_action_date)}</p>
  </div>
  
  <div style="border: 1px solid #e5e7eb; padding: 16px; border-radius: 8px;">
    <h3>Last Action</h3>
    <p>{bill.last_action}</p>
  </div>
</div>

## Description

<div class="texas-impact-description">
  {bill.texas_impact_description}
</div>

## Links

<div style="display: flex; gap: 16px; margin: 24px 0;">
  <a href={bill.url} target="_blank" style="text-decoration: none;">
    <button style="background-color: #4682B4; color: white; border: none; padding: 10px 16px; border-radius: 4px; cursor: pointer; font-weight: 500;">
      View Bill on Texas Legislature Online
    </button>
  </a>
  
  <a href={bill.bill_text_link} target="_blank" style="text-decoration: none;">
    <button style="background-color: #4682B4; color: white; border: none; padding: 10px 16px; border-radius: 4px; cursor: pointer; font-weight: 500;">
      View Bill Text
    </button>
  </a>
</div>

## Authors

<DataTable 
  data={bill_detail} 
>
  <Column id=authors title="Authors" />
  <Column id=sponsors title="Sponsors" />
  <Column id=coauthors title="Coauthors" />
  <Column id=cosponsors title="Cosponsors" />
</DataTable>

---

<small>Last updated: {new Date().toLocaleDateString()}</small>

<div style="margin-top: 32px;">
  <a href="/" style="text-decoration: none;">
    <button style="background-color: #f5f5f5; color: #333; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; font-weight: 500;">
      ← Back to Dashboard
    </button>
  </a>
</div> 