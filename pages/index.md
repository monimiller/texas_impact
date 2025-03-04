---
title: Texas Impact Legislative Dashboard
queries:
  - all_bills: all_bills.sql
  - progress_counts: progress_counts.sql
  - progress_stages: progress_stages.sql
  - topic_counts: topic_counts.sql
  - total_count: total_count.sql
  - house_count: house_count.sql
  - senate_count: senate_count.sql
  - support_count: support_count.sql
  - oppose_count: oppose_count.sql
  - position_chamber_topic_sankey: position_chamber_topic_sankey.sql
  - chamber_position_topic_sankey: chamber_position_topic_sankey.sql
  - position_topic_chamber_sankey: position_topic_chamber_sankey.sql
---

<BigValue 
  data={total_count} 
  value="value" 
  title="Total Bills Tracked" 
  subtitle="across all chambers"
/>

<Grid columnsWide={2}>
  <BigValue 
    data={house_count} 
    value="value" 
    title="House Bills" 
  />
  <BigValue 
    data={senate_count} 
    value="value" 
    title="Senate Bills" 
  />
</Grid>

<Grid columnsWide={2}>
  <BigValue 
    data={support_count} 
    value="value"
    title="Bills We Support" 
  />
  <BigValue 
    data={oppose_count} 
    value="value"
    title="Bills We Oppose" 
  />
</Grid>

## Bill Progress Overview

<FunnelChart
  data={progress_stages}
  nameCol=stage
  valueCol=count
  title="Bill Progress Through Legislative Stages"
  subtitle="Number of bills at each stage of the legislative process"
  sort="none"
  showPercent={true}
  chartAreaHeight={350}
/>

## Bills Flow Analysis

<Tabs>
  <Tab label="Position → Chamber → Topic">
    <SankeyDiagram
      data={position_chamber_topic_sankey}
      sourceCol="source"
      targetCol="target"
      valueCol="value"
      title="Bills: Position → Chamber → Topic"
      subtitle="Flow from our position, to the legislative chamber, to the topic"
      chartAreaHeight={500}
      colorPalette={[
        "#2E8B57", // Support - Sea Green
        "#CD5C5C", // Oppose - Indian Red
        "#4682B4", // House - Steel Blue
        "#9370DB", // Senate - Medium Purple
        "#20B2AA", // Topic 1 - Light Sea Green
        "#6495ED", // Topic 2 - Cornflower Blue
        "#DEB887", // Topic 3 - Burlywood
        "#BA55D3"  // Topic 4 - Medium Orchid
      ]}
    />
  </Tab>
  <Tab label="Chamber → Position → Topic">
    <SankeyDiagram
      data={chamber_position_topic_sankey}
      sourceCol="source"
      targetCol="target"
      valueCol="value"
      title="Bills: Chamber → Position → Topic"
      subtitle="Flow from legislative chamber, to our position, to the topic"
      chartAreaHeight={500}
      colorPalette={[
        "#4682B4", // House - Steel Blue
        "#9370DB", // Senate - Medium Purple
        "#2E8B57", // Support - Sea Green
        "#CD5C5C", // Oppose - Indian Red
        "#20B2AA", // Topic 1 - Light Sea Green
        "#6495ED", // Topic 2 - Cornflower Blue
        "#DEB887", // Topic 3 - Burlywood
        "#BA55D3"  // Topic 4 - Medium Orchid
      ]}
    />
  </Tab>
  <Tab label="Position → Topic → Chamber">
    <SankeyDiagram
      data={position_topic_chamber_sankey}
      sourceCol="source"
      targetCol="target"
      valueCol="value"
      title="Bills: Position → Topic → Chamber"
      subtitle="Flow from our position, to the topic, to the legislative chamber"
      chartAreaHeight={500}
      colorPalette={[
        "#2E8B57", // Support - Sea Green
        "#CD5C5C", // Oppose - Indian Red
        "#20B2AA", // Topic 1 - Light Sea Green
        "#6495ED", // Topic 2 - Cornflower Blue
        "#DEB887", // Topic 3 - Burlywood
        "#BA55D3", // Topic 4 - Medium Orchid
        "#4682B4", // House - Steel Blue
        "#9370DB"  // Senate - Medium Purple
      ]}
    />
  </Tab>
</Tabs>

## Bill Topics

<BarChart 
  data={topic_counts} 
  x="topic_name" 
  y="bill_count"
  title="Bills by Topic"
  subtitle="Click on a topic to see detailed information"
  sort="desc"
  chartAreaHeight={350}
/>

<DataTable 
  data={topic_counts}
  link="topic_link"
  title="Topics with Bill Counts"
>
  <Column id="topic_name" title="Topic" />
  <Column id="bill_count" title="Number of Bills" />
  <Column id="active_bills" title="Active Bills" />
</DataTable>

<Accordion title="All Topics List">
  {#each topic_counts as topic}
  - [{topic.topic_name}](/topic/{topic.topic_name}) ({topic.bill_count} bills)
  {/each}
</Accordion>

## Recent Activity

<DataTable 
  data={all_bills.limit(5)} 
  search=true
  formatColumnTitles=true
  defaultSort="last_action_date"
  defaultSortDirection="desc"
  link=bill_detail_url
>
  <Column id=bill_number title="Bill Number" />
  <Column id=chamber title="Chamber" />
  <Column id=Position title="Position" />
  <Column id=Topic title="Topic" />
  <Column id=status_field title="Status" />
  <Column id=last_action_date title="Last Updated" />
  <Column id=last_action title="Last Action" />
</DataTable>

---

<small>Last updated: {new Date().toLocaleDateString()}</small>
