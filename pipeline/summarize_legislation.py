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

    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        # api_key="my_api_key",
    )

    # Replace placeholders like {{JSON_INPUT}} with real values,
    # because the SDK does not support variables.
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
                        "text": f'You will be summarizing and analyzing legislative information about period care mandates for a specific state. The information is provided in a JSON format. Your task is to summarize the documents and legislative links, then provide an overall assessment of the state\'s support for menstrual care accessibility in a fun "Zoomer" tone.\n\nHere\'s the JSON input containing the legislative information:\n\n<json_input>\n{bill_texts}\n</json_input>\n\nFollow these steps to complete the task:\n\n1. Parse the JSON input and extract the relevant information about bills, documents, and legislative links related to period care mandates.\n\n2. Summarize each bill and document briefly, focusing on key points such as:\n   - The main purpose of the bill\n   - Proposed changes or mandates\n   - Target locations (e.g., schools, public buildings)\n   - Any specific products or services mentioned\n\n3. Analyze the overall legislative support for menstrual care accessibility in the state by considering:\n   - The number of bills proposed\n   - The content and intent of the bills\n   - Any patterns or trends in the legislation\n   - The current status of the bills (e.g., passed, pending, failed)\n\n4. Based on your analysis, determine whether the state appears to be supportive, neutral, or unsupportive of menstrual care accessibility.\n\n5. Prepare a summary of your findings in a fun "Zoomer" tone. This means:\n   - Use casual, conversational language\n   - Include relevant slang or internet-speak (e.g., "ngl", "fr", "lowkey")\n   - Add some humor or playful comments\n   - Use emojis sparingly but effectively\n   - Keep it brief and to the point\n\n6. Structure your response as follows:\n\n<summary>\n[Insert your summary of the bills and documents here]\n</summary>\n\n<analysis>\n[Insert your analysis of the overall legislative support here]\n</analysis>\n\n<zoomer_vibe>\n[Insert your fun "Zoomer" tone summary here]\n</zoomer_vibe>\n\nRemember to maintain accuracy and respect for the subject matter while adopting the "Zoomer" tone in the final section.',
                    }
                ],
            }
        ],
    )
    print(message.content)


def main():
    states = {}
    bills = pl.read_csv("../sources/legiscan/bills.csv")

    results = pl.DataFrame(
        {"state": pl.Series([], dtype=pl.Utf8), "vibe": pl.Series([], dtype=pl.Utf8)}
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
        results = results.vstack(pl.DataFrame({"state": [state], "vibe": [vibe]}))
        time.sleep(1)  # Be nice to the API

        results.write_csv(
            "../sources/generated/state_period_care_vibes.csv",
            separator=",",
            include_header=True,
        )


if __name__ == "__main__":
    main()
