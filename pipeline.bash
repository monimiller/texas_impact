#!/usr/bin/env bash

APIKEY="915b8d36efc1524035bf6336561b07e6"
# Fetch bills related to Feminine Hygiene from LegiScan API
page=1
while true; do
    data=$(curl -G "https://api.legiscan.com/" \
        --data-urlencode "key=$APIKEY" \
        --data-urlencode "op=getSearch" \
        --data-urlencode "state=ALL" \
        --data-urlencode "year=4" \
        --data-urlencode "page=$page" \
        --data-urlencode "query=Feminine Hygiene" | jq -c '
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
        ')

    if [ -z "$data" ]; then
        break
    fi

    echo "$data" | duckdb -c "
        CREATE TABLE new_bills AS
        SELECT * FROM read_json_auto('/dev/stdin');
        
        CREATE TABLE IF NOT EXISTS bills AS
        SELECT * FROM 'sources/legiscan/bills.csv';
        
        INSERT INTO bills SELECT * FROM new_bills;
    
        COPY bills TO 'sources/legiscan/bills.csv' (HEADER, DELIMITER ',');
    "

    page=$((page + 1))
done