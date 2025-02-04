# getBill
Description:
This operation returns the primary bill detail information including sponsors, committee references, full history, bill
text and roll call information.
Input Parameters:
Name Value
id Retrieve bill detail information for bill_id as given by id
Pull API Template:
https://api.legiscan.com/?key=APIKEY&op=getBill&id=BILL_ID
Client Source Code:
https://api.legiscan.com/docs/class-LegiScan_Process.html
Response:
Detail bill information object enumerating associated information along with sponsor people_id, bill text doc_id and
voting roll_call_id. The change_hash is a representation of the current bill version, it should be stored for a quick
comparison to subsequent getMasterListRaw calls to detect when bills have changed and need updating.