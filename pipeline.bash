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
    CREATE TABLE bills AS
    SELECT * FROM read_json_auto('/dev/stdin');
    COPY bills TO 'bills.csv' (HEADER, DELIMITER ',');
"
