# /// script
# requires-python = "<3.13"
# dependencies = [
#   "requests",
#   "anthropic",
#   "polars",
# ]
# ///

import anthropic
import csv
import requests
import time
import os
import hashlib
import json
import polars as pl
import re

# Get the Legiscan API key from the environment
LEGISCAN_API_KEY = os.getenv("LEGISCAN_API_KEY")
if not LEGISCAN_API_KEY:
    raise ValueError("LEGISCAN_API_KEY environment variable is not set")


def fetch_bill_text(bill_id):
    try:
        # https://api.legiscan.com/?key=APIKEY&op=getBill&id=BILL_ID
        response = requests.get(
            "https://api.legiscan.com/",
            params={"key": LEGISCAN_API_KEY, "op": "getBill", "id": bill_id},
        )
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching bill text: {e}")
        return None


def SummarizeBills(state, bill_texts):
    """Analyze bills related to period care and feminine hygiene products."""

    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"You will be summarizing and analyzing legislative information about period care mandates for a specific state. The information is provided in a JSON format. Your task is to summarize the documents and legislative links, then provide an overall assessment of the state's support for menstrual care accessibility in a fun \"Zoomer\" tone.\n\nHere's the JSON input containing the legislative information:\n\n<json_input>\n{bill_texts}\n</json_input>\n\n[... rest of the prompt ...]",
                    }
                ],
            }
        ],
    )

    response = message.content[0].text

    # Parse the response
    summary = re.search(r"<summary>(.*?)</summary>", response, re.DOTALL)
    analysis = re.search(r"<analysis>(.*?)</analysis>", response, re.DOTALL)
    zoomer_vibe = re.search(r"<zoomer_vibe>(.*?)</zoomer_vibe>", response, re.DOTALL)

    return {
        "summary": summary.group(1).strip() if summary else "",
        "analysis": analysis.group(1).strip() if analysis else "",
        "zoomer_vibe": zoomer_vibe.group(1).strip() if zoomer_vibe else "",
    }


def main():
    bills = pl.read_csv("../sources/legiscan/bills.csv")

    results = pl.DataFrame(
        {
            "state": pl.Series([], dtype=pl.Utf8),
            "summary": pl.Series([], dtype=pl.Utf8),
            "analysis": pl.Series([], dtype=pl.Utf8),
            "zoomer_vibe": pl.Series([], dtype=pl.Utf8),
        }
    )

    # Sort states from least number of bills to most
    state_bill_counts = bills.group_by("state").agg(
        pl.count("bill_id").alias("bill_count")
    )
    sorted_states = state_bill_counts.sort("bill_count").select("state")

    for state in sorted_states["state"]:
        print(f"Processing {state}...")
        state_bills = bills.filter(pl.col("state") == state)
        bill_texts = []

        for bill in state_bills.iter_rows(named=True):
            text = fetch_bill_text(bill["bill_id"])
            if text:
                bill_texts.append(
                    f"Bill {bill['bill_number']}: {text[:1000]}..."
                )  # Truncate to first 1000 chars

        vibe = SummarizeBills(state, " ".join(bill_texts))
        results = results.vstack(
            pl.DataFrame(
                {
                    "state": [state],
                    "summary": [vibe["summary"]],
                    "analysis": [vibe["analysis"]],
                    "zoomer_vibe": [vibe["zoomer_vibe"]],
                }
            )
        )
        time.sleep(1)  # Be nice to the API

        results.write_csv(
            "../sources/generated/state_period_care_vibes.csv",
            separator=",",
            include_header=True,
        )


if __name__ == "__main__":
    main()
