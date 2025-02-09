#!/usr/bin/env -S uv run --script
# /// script
# requires-python = "<3.13"
# dependencies = [
#   "requests",
#   "pandas>=2.0.0",
#   "python-dotenv",
#   "dlt[filesystem]",
# ]
# ///
import os
import dlt
import pandas as pd
import requests
from typing import Dict, List, Iterator
from urllib.parse import urlencode
from dotenv import load_dotenv

@dlt.source
def legiscan_source(api_key: str):
    """DLT source for Legiscan API data"""
    
    @dlt.resource(
        write_disposition="replace",
        primary_key=["bill_id"],
        name="monitored_bills"
    )
    def get_monitored_bills() -> Iterator[Dict]:
        """Resource that gets all monitored bills"""
        params = {
            'key': api_key,
            'op': 'getMonitorList',
            'record': 'all'
        }
        url = f"https://api.legiscan.com/?{urlencode(params)}"
        print(f"Requesting monitored bills: {url}")
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                bills = data.get('monitorlist', [])
                print(f"Found {len(bills)} bills in the monitor list")
                for bill in bills:
                    yield bill
            else:
                print(f"API Error: {data.get('alert', 'Unknown error')}")
    
    @dlt.resource(
        write_disposition="replace",
        primary_key=["bill_id"],
        name="bill_details"
    )
    def get_bill_details() -> Iterator[Dict]:
        """Resource that gets detailed information for each monitored bill"""
        # First get all monitored bills
        params = {
            'key': api_key,
            'op': 'getMonitorList',
            'record': 'all'
        }
        response = requests.get(f"https://api.legiscan.com/?{urlencode(params)}")
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                bills = data.get('monitorlist', [])
                
                # Now get details for each bill
                for bill in bills:
                    bill_id = bill['bill_id']
                    params = {
                        'key': api_key,
                        'op': 'getBill',
                        'id': bill_id
                    }
                    url = f"https://api.legiscan.com/?{urlencode(params)}"
                    print(f"Requesting details for bill {bill_id}: {url}")
                    
                    bill_response = requests.get(url)
                    if bill_response.status_code == 200:
                        bill_data = bill_response.json()
                        if bill_data['status'] == 'OK':
                            yield bill_data['bill']
                        else:
                            print(f"API Error for bill {bill_id}: {bill_data.get('alert', 'Unknown error')}")
                    else:
                        print(f"HTTP Error {bill_response.status_code} for bill {bill_id}")
            else:
                print(f"API Error: {data.get('alert', 'Unknown error')}")
    
    return [get_monitored_bills, get_bill_details]

def main():
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv('LEGISCAN_API_KEY')
    if not api_key:
        print("Error: LEGISCAN_API_KEY not found in environment variables")
        return
    
    # Initialize pipeline with filesystem destination
    pipeline = dlt.pipeline(
        pipeline_name="legiscan",
        destination='filesystem',
        dataset_name='pipeline',
        dev_mode=True  # This replaces full_refresh=True
    )
    
    # Create source with credentials
    source = legiscan_source(api_key=api_key)
    
    # Run pipeline
    print("Starting pipeline...")
    info = pipeline.run(source)
    
    print(f"\nPipeline completed! Load info:")
    print(info)
    
    # Load the CSVs for stats
    monitored_df = pd.read_csv('pipeline/monitored_bills.csv')
    details_df = pd.read_csv('pipeline/bill_details.csv')
    
    print(f"\nStats:")
    print(f"Monitored bills: {len(monitored_df)}")
    print(f"Bill details: {len(details_df)}")
    
    if 'state' in details_df.columns:
        print("\nBills by state:")
        print(details_df['state'].value_counts())
    
    if 'status' in details_df.columns:
        print("\nBills by status:")
        print(details_df['status'].value_counts())

if __name__ == "__main__":
    main()
