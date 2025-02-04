#!/usr/bin/env -S uv run --script
# /// script
# requires-python = "<3.13"
# dependencies = [
#   "requests",
#   "pandas>=2.0.0",
# ]
# ///
import pandas as pd
import requests
from typing import Dict, List
from urllib.parse import urlencode

def fetch_monitored_bills(api_key: str) -> List[Dict]:
    """Fetch all monitored bills from Legiscan API"""
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
            # Extract bills from the monitor list
            bills = data.get('monitorlist', [])
            print(f"Found {len(bills)} bills in the monitor list")
            return bills
        else:
            print(f"API Error: {data.get('alert', 'Unknown error')}")
    else:
        print(f"HTTP Error: {response.status_code}")
    return []

def main():
    # API key
    api_key = ""
    
    # Fetch all monitored bills
    print("Fetching monitored bills...")
    bills = fetch_monitored_bills(api_key)
    
    if bills:
        # Convert to DataFrame and save to CSV
        df = pd.DataFrame(bills)
        df.to_csv('pipeline/monitored_bills.csv', index=False)
        print(f"\nSaved {len(bills)} monitored bills to monitored_bills.csv")
        
        # Print some basic stats
        print("\nBill Statistics:")
        if 'state' in df.columns:
            print("\nBills by state:")
            print(df['state'].value_counts())
        if 'status' in df.columns:
            print("\nBills by status:")
            print(df['status'].value_counts())
    else:
        print("\nNo monitored bills were found")

if __name__ == "__main__":
    main()
