# /// script
# dependencies = [
#     "dlt[duckdb]",
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
        bills.append(
            {
                "bill_id": bill["bill_id"],
                "number": bill["number"],
                "state": bill["state"],
                "status": bill["status"],
                "title": bill["title"],
                "description": bill["description"],
                "last_action": bill["last_action"],
                "last_action_date": bill["last_action_date"],
            }
        )

    return bills


def get_bill_details(api_key: str, bill_id: str) -> Dict:
    """Fetch details for a specific bill"""
    url = "https://api.legiscan.com/"
    params = {"key": api_key.strip(), "op": "getBill", "id": bill_id}

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    bill_data = data.get("bill", {})
    return {
        "bill_id": bill_data.get("bill_id"),
        "number": bill_data.get("bill_number"),
        "state": bill_data.get("state"),
        "status": bill_data.get("status"),
        "title": bill_data.get("title"),
        "description": bill_data.get("description"),
        "last_action": bill_data.get("last_action"),
        "last_action_date": bill_data.get("last_action_date"),
    }


@dlt.source
def legiscan_source(api_key: str = os.getenv("LEGISCAN_API_KEY")):
    """DLT source for Legiscan data"""
    if not api_key:
        raise ValueError("LEGISCAN_API_KEY environment variable is not set")

    @dlt.resource
    def bills():
        # First get the monitor list
        monitor_list = get_monitor_list(api_key)

        # Then get details for each bill
        for bill in monitor_list:
            bill_details = get_bill_details(api_key, bill["bill_id"])
            yield bill_details

    # Return the resource
    return bills


# Pipeline execution
if __name__ == "__main__":
    # Create output directory if it doesn't exist
    LEGISCAN_DIR.mkdir(parents=True, exist_ok=True)

    # Initialize the pipeline with DuckDB destination
    pipeline = dlt.pipeline(
        pipeline_name="legiscan",
        destination=dlt.destinations.duckdb(str(LEGISCAN_DIR / "bills.duckdb")),
        dataset_name="legiscan_bills",
    )

    # Load the data
    load_info = pipeline.run(legiscan_source())

    # Create a view for the latest data
    with pipeline.sql_client() as client:
        # Create the schema if it doesn't exist
        client.execute("CREATE SCHEMA IF NOT EXISTS legiscan_bills")

        # Get the latest schema name
        latest_schema = client.execute("""
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name LIKE 'legiscan_bills_%' 
            ORDER BY schema_name DESC 
            LIMIT 1
        """).fetchone()[0]

        # Create or replace view
        client.execute(f"""
            CREATE OR REPLACE VIEW legiscan_bills.latest_bills AS 
            SELECT * FROM {latest_schema}.bills
        """)

    # Print outcome
    print(load_info)
