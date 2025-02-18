#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#     "dlt",
#     "requests",
#     "python-dotenv",
# ]
# ///

import dlt
from typing import Dict, List
import requests
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Set up filesystem paths
PROJECT_ROOT = Path(__file__).parent
LEGISCAN_DIR = PROJECT_ROOT / "sources" / "legiscan"


def get_monitor_list(api_key: str) -> List[Dict]:
    """Fetch the monitor list from LegiscanAPI"""
    url = "https://api.legiscan.com/"
    params = {"key": api_key.strip(), "op": "getMonitorList", "state": "TX"}

    response = requests.get(url, params=params)
    response.raise_for_status()

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"Failed to decode JSON. Response content: {response.text}")
        raise

    # Extract and transform bills from monitorlist, including all relevant fields
    bills = []
    for bill in data.get("monitorlist", []):
        bills.append({
            "bill_id": bill["bill_id"],
            "number": bill["number"],
            "state": bill["state"],
            "status": bill["status"],
            "title": bill["title"],
            "description": bill["description"],
            "last_action": bill["last_action"],
            "last_action_date": bill["last_action_date"]
        })

    return bills


def get_bill_details(api_key: str, bill_id: str) -> Dict:
    """
    Fetch details for a specific bill
    
    Args:
        api_key: LegiscanAPI key
        bill_id: ID of the bill to fetch
        
    Returns:
        Dictionary containing bill details with nested data
    """
    url = "https://api.legiscan.com/"
    params = {"key": api_key.strip(), "op": "getBill", "id": str(bill_id)}

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    bill_data = data.get("bill", {})
    
    # Return the complete bill data
    return bill_data


@dlt.source(root_key=True)
def legiscan_source(api_key: str = os.getenv("LEGISCAN_API_KEY")):
    """DLT source for Legiscan data with nested tables"""
    if not api_key:
        raise ValueError("LEGISCAN_API_KEY environment variable is not set")

    @dlt.resource(primary_key="bill_id")
    def bills():
        """Root resource for bills"""
        monitor_list = get_monitor_list(api_key)
        for bill in monitor_list:
            bill_details = get_bill_details(api_key, bill["bill_id"])
            yield bill_details

    @dlt.resource(name="bill_history")
    def history():
        """History events for bills"""
        monitor_list = get_monitor_list(api_key)
        for bill in monitor_list:
            bill_details = get_bill_details(api_key, bill["bill_id"])
            history = bill_details.get("history", [])
            for event in history:
                event["bill_id"] = bill_details["bill_id"]
                event["date"] = event.get("date")
                event["action"] = event.get("action")
                event["chamber"] = event.get("chamber")
                event["chamber_id"] = event.get("chamber_id")
                event["importance"] = event.get("importance")
                yield event

    @dlt.resource(name="bill_sponsors")
    def sponsors():
        """Sponsors for bills"""
        monitor_list = get_monitor_list(api_key)
        for bill in monitor_list:
            bill_details = get_bill_details(api_key, bill["bill_id"])
            sponsors = bill_details.get("sponsors", [])
            for sponsor in sponsors:
                sponsor["bill_id"] = bill_details["bill_id"]
                sponsor["people_id"] = sponsor.get("people_id")
                sponsor["person_hash"] = sponsor.get("person_hash")
                sponsor["party_id"] = sponsor.get("party_id")
                sponsor["party"] = sponsor.get("party")
                sponsor["role_id"] = sponsor.get("role_id")
                sponsor["role"] = sponsor.get("role")
                sponsor["name"] = sponsor.get("name")
                sponsor["first_name"] = sponsor.get("first_name")
                sponsor["middle_name"] = sponsor.get("middle_name")
                sponsor["last_name"] = sponsor.get("last_name")
                sponsor["suffix"] = sponsor.get("suffix")
                sponsor["nickname"] = sponsor.get("nickname")
                sponsor["district"] = sponsor.get("district")
                sponsor["ftm_eid"] = sponsor.get("ftm_eid")
                sponsor["votesmart_id"] = sponsor.get("votesmart_id")
                sponsor["opensecrets_id"] = sponsor.get("opensecrets_id")
                sponsor["knowwho_pid"] = sponsor.get("knowwho_pid")
                sponsor["ballotpedia"] = sponsor.get("ballotpedia")
                sponsor["sponsor_type_id"] = sponsor.get("sponsor_type_id")
                sponsor["sponsor_order"] = sponsor.get("sponsor_order")
                sponsor["committee_sponsor"] = sponsor.get("committee_sponsor")
                sponsor["committee_id"] = sponsor.get("committee_id")
                sponsor["state_federal"] = sponsor.get("state_federal")
                yield sponsor

    @dlt.resource(name="bill_subjects")
    def subjects():
        """Subjects for bills"""
        monitor_list = get_monitor_list(api_key)
        for bill in monitor_list:
            bill_details = get_bill_details(api_key, bill["bill_id"])
            subjects = bill_details.get("subjects", [])
            for subject in subjects:
                subject["bill_id"] = bill_details["bill_id"]
                subject["subject_id"] = subject.get("subject_id")
                subject["subject_name"] = subject.get("subject_name")
                yield subject

    # Return all resources
    return [bills, history, sponsors, subjects]


# Pipeline execution
if __name__ == "__main__":
    # Create output directory if it doesn't exist
    LEGISCAN_DIR.mkdir(parents=True, exist_ok=True)

    # Initialize the pipeline with filesystem destination
    pipeline = dlt.pipeline(
        pipeline_name="legiscan",
        destination="filesystem",
        dataset_name="legiscan_bills",
        dev_mode=False
    )

    # Load the data with CSV format
    load_info = pipeline.run(legiscan_source(), loader_file_format="csv")

    # Print outcome
    print(load_info)
