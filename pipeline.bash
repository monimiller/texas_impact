#!/usr/bin/env bash

APIKEY="915b8d36efc1524035bf6336561b07e6"
# Fetch bills related to Feminine Hygiene from LegiScan API
page=1
while true; do
    data=$(curl -G "https://api.legiscan.com/" \
        --data-urlencode "key=$APIKEY" \
        --data-urlencode "op=getSearch" \
        --data-urlencode "state=ALL" \
        --data-urlencode "year=2" \
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
        SELECT DISTINCT * FROM read_json_auto('/dev/stdin');
        
        CREATE TABLE IF NOT EXISTS bills AS
        SELECT DISTINCT * FROM 'sources/legiscan/bills.parquet';
        
        INSERT INTO bills SELECT DISTINCT * FROM new_bills;
    
        COPY (SELECT * FROM bills ORDER BY bill_id) TO 'sources/legiscan/bills.parquet' (FORMAT PARQUET);
    "

    page=$((page + 1))
done