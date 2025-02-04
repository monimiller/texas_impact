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

def fetch_bill_details(bill_number: str, api_key: str) -> Dict:
    """Fetch bill details from Legiscan API"""
    response = requests.get(
        'https://api.legiscan.com/',
        params={
            'key': api_key,
            'op': 'getBill',
            'id': bill_number
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK':
            return data['bill']
    return None

def main():
    # Read input bills
    input_bills = pd.read_csv('pipeline/bills.csv')
    
    # List to store bill details
    bill_details = []
    
    # API key
    api_key = ""
    
    # Process each bill
    for _, row in input_bills.iterrows():
        bill_number = row['Bill Number']
        print(f"Processing bill {bill_number}")
        
        bill_data = fetch_bill_details(bill_number, api_key)
        if bill_data:
            bill_details.append(bill_data)
    
    # Convert to DataFrame and save to CSV
    if bill_details:
        df = pd.DataFrame(bill_details)
        df.to_csv('pipeline/bills_details.csv', index=False)
        print(f"Saved {len(bill_details)} bill details to bills_details.csv")
    else:
        print("No bill details were found")

if __name__ == "__main__":
    main()
