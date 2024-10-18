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
        return response.json()
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
                        "text": f'You will be summarizing and analyzing legislative information about period care mandates for a specific state. The information is provided in a JSON format. Your task is to summarize the documents and legislative links, then provide an overall assessment of the state\'s support for menstrual care accessibility in a fun "Zoomer" tone.\n\nHere\'s the JSON input containing the legislative information:\n\n<json_input>\n{bill_texts}\n</json_input>\n\nFollow these steps to complete the task:\n\n1. Parse the JSON input and extract the relevant information about bills, documents, and legislative links related to period care mandates.\n\n2. Summarize each bill and document briefly, focusing on key points such as:\n   - The main purpose of the bill\n   - Proposed changes or mandates\n   - Target locations (e.g., schools, public buildings)\n   - Any specific products or services mentioned\n\n3. Analyze the overall legislative support for menstrual care accessibility in the state by considering:\n   - The number of bills proposed\n   - The content and intent of the bills\n   - Any patterns or trends in the legislation\n   - The current status of the bills (e.g., passed, pending, failed)\n\n4. Based on your analysis, determine whether the state appears to be supportive, neutral, or unsupportive of menstrual care accessibility.\n\n5. Prepare a summary of your findings in a fun "Zoomer" tone. This means:\n   - Use casual, conversational language\n   - Include relevant slang or internet-speak (e.g., "ngl", "fr", "lowkey")\n   - Add some humor or playful comments\n   - Use emojis sparingly but effectively\n   - Keep it brief and to the point\n\n6. Structure your response as follows:\n\n<summary><br>[Insert your summary of the bills and documents here]<br></summary><br><br><analysis><br>[Insert your analysis of the overall legislative support here]<br></analysis><br><br><zoomer_vibe><br>[Insert your fun "Zoomer" tone summary here]<br></zoomer_vibe>\n\nRemember to maintain accuracy and respect for the subject matter while adopting the "Zoomer" tone in the final section.',
                    }
                ],
            }
        ],
    )

    response = message.content[0].text
    print("AI Response:", response)  # Debug print

    # If the response doesn't contain tags, we'll treat the whole response as the zoomer_vibe
    if (
        "<summary>" not in response
        and "<analysis>" not in response
        and "<zoomer_vibe>" not in response
    ):
        return {
            "summary": "",
            "analysis": "",
            "zoomer_vibe": response.strip(),
        }

    # Parse the response if tags are present
    summary = re.search(r"<summary>(.*?)</summary>", response, re.DOTALL)
    analysis = re.search(r"<analysis>(.*?)</analysis>", response, re.DOTALL)
    zoomer_vibe = re.search(r"<zoomer_vibe>(.*?)</zoomer_vibe>", response, re.DOTALL)

    return {
        "summary": summary.group(1).strip() if summary else "",
        "analysis": analysis.group(1).strip() if analysis else "",
        "zoomer_vibe": zoomer_vibe.group(1).strip()
        if zoomer_vibe
        else response.strip(),
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

        # Parse out the actual bill text from the legiscan response
        for bill in state_bills.iter_rows(named=True):
            bill_json = fetch_bill_text(bill["bill_id"])
            if bill_json:
                print("Bill info:", bill_json)
                # Extract relevant information from the API response
                bill_info = bill_json.get("bill", {})
                bill_title = bill_info.get("title", "")
                bill_description = bill_info.get("description", "")
                # TODO Could read PDFs in
                # bill_texts = bill_info.get("texts", [])

                # Combine the relevant information
                combined_text = (
                    f"Title: {bill_title}\nDescription: {bill_description}\n"
                )

                # Truncate the combined text to a reasonable length
                truncated_text = combined_text[
                    :2000
                ]  # Increased from 1000 to 2000 chars

                bill_texts.append(f"Bill {bill['bill_number']}:\n{truncated_text}")

        print(" ".join(bill_texts))

        vibe = SummarizeBills(state, " ".join(bill_texts))
        print("Vibe result:", vibe)  # Debug print

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
            quote_char='"',
            escape_char="\\",
        )


if __name__ == "__main__":
    main()
