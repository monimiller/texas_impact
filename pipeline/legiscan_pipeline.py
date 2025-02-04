
import dlt
import pandas as pd
import requests
from typing import Dict, Iterator

# Initialize pipeline
pipeline = dlt.pipeline(pipeline_name="legiscan", destination='duckdb', dataset_name='bills_data')

@dlt.source
def legiscan_source(api_key: str):
    """
    DLT source for Legiscan API data
    """
    
    @dlt.resource(
        write_disposition="replace",
        primary_key=["bill_id"]
    )
    def get_bills(bills_csv: str) -> Iterator[Dict]:
        """
        Resource that reads bills from CSV and fetches their details from Legiscan
        """
        # Read bills from CSV
        df = pd.read_csv(bills_csv)
        
        # For each bill
        for _, row in df.iterrows():
            bill_number = row['Bill Number']
            
            # Make API request
            response = requests.get(
                'https://api.legiscan.com/',
                params={
                    'key': api_key,
                    'op': 'getBill',
                    'id': bill_number  # This might need to be adjusted if bill_number is not the ID
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'OK':
                    yield data['bill']
            
    return get_bills

def main():
    # Create source with credentials
    source = legiscan_source(
        api_key="915b8d36efc1524035bf6336561b07e6"  # In production, use environment variables
    )
    
    # Run pipeline
    load_info = pipeline.run(
        source.get_bills(bills_csv='pipeline/bills.csv')
    )
    
    print(f"Load info: {load_info}")

if __name__ == "__main__":
    main()
