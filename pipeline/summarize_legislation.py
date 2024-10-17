# /// script
# requires-python = "<3.13"
# dependencies = [
#   "requests",
#   "dspy-ai",
# ]
# ///

import csv
import requests
import dspy
import time
import os

# Set up DSPy
dspy.settings.configure(lm=dspy.OpenAI(model="gpt-3.5-turbo"))

# Get the Legiscan API key from the environment
LEGISCAN_API_KEY = os.getenv("LEGISCAN_API_KEY")
if not LEGISCAN_API_KEY:
    raise ValueError("LEGISCAN_API_KEY environment variable is not set")


import hashlib
import json


def get_cache_filename(bill_id):
    return f".cache/{hashlib.md5(bill_id.encode()).hexdigest()}.json"


def fetch_bill_text(bill_id):
    cache_filename = get_cache_filename(bill_id)

    # Check if the response is cached
    if os.path.exists(cache_filename):
        with open(cache_filename, "r") as cache_file:
            return json.load(cache_file)

    try:
        # https://api.legiscan.com/?key=APIKEY&op=getBill&id=BILL_ID
        response = requests.get(
            "https://api.legiscan.com/",
            params={"key": LEGISCAN_API_KEY, "op": "getBill", "id": bill_id},
        )
        response.raise_for_status()
        bill_text = response.text

        # Cache the response
        os.makedirs(".cache", exist_ok=True)
        with open(cache_filename, "w") as cache_file:
            json.dump(bill_text, cache_file)

        return bill_text
    except requests.RequestException as e:
        print(f"Error fetching bill text: {e}")
        return None


class SummarizeBills(dspy.Signature):
    """Analyze bills related to period care and feminine hygiene products."""

    state = dspy.InputField()
    bill_texts = dspy.InputField()
    vibe = dspy.OutputField(
        desc="Overall 'vibe' or sentiment of the legislation for period care in this state"
    )


class BillAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.summarize = dspy.Predict(SummarizeBills)

    def forward(self, state, bill_texts):
        result = self.summarize(state=state, bill_texts=bill_texts)
        return result.vibe


def main():
    states = {}
    with open("../sources/legiscan/bills.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["state"] not in states:
                states[row["state"]] = []
            states[row["state"]].append(row)

    analyzer = BillAnalyzer()
    results = []

    for state, bills in states.items():
        print(f"Processing {state}...")
        bill_texts = []
        for bill in bills:
            text = fetch_bill_text(bill["bill_id"])
            if text:
                bill_texts.append(
                    f"Bill {bill['bill_number']}: {text[:1000]}..."
                )  # Truncate to first 1000 chars

        vibe = analyzer(state, " ".join(bill_texts))
        results.append({"state": state, "vibe": vibe})
        time.sleep(1)  # Be nice to the API

    with open(
        "../sources/generated/state_period_care_vibes.csv", "w", newline=""
    ) as file:
        writer = csv.DictWriter(file, fieldnames=["state", "vibe"])
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    main()
