#!/usr/bin/env bash

curl -G "https://api.legiscan.com/" \
    --data-urlencode "key=$APIKEY" \
    --data-urlencode "op=getSearch" \
    --data-urlencode "state=ALL" \
    --data-urlencode "query=Feminine Hygiene" |
    jq -c '
    .searchresult |
    to_entries[] |
    select(.key | tonumber? != null) |
    .value |
    {
        state,
        bill_number,
        bill_id,
        url,
        text_url,
        last_action_date,
        last_action,
        title
    }
' | duckdb -c "
    CREATE TABLE new_bills AS
    SELECT * FROM read_json_auto('/dev/stdin');
    
    CREATE TABLE IF NOT EXISTS bills AS
    SELECT * FROM 'hf_stats/bills.csv';
    
    INSERT INTO bills SELECT * FROM new_bills;
    
    COPY bills TO 'hf_stats/bills.csv' (HEADER, DELIMITER ',');
"