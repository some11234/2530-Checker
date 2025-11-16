import os
import re
import requests

UVM_URL = "https://soc.uvm.edu/api/?page=fose&route=details"

BODY = {
    "group": "code:HLTH 2530",
    "key": "crn:14157",
    "srcdb": "202601",
    "matched": ""
}

HEADERS = {
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "UVM-Seat-Checker/1.0 (personal; 1req/5min)"
}

WEBHOOK_URL = os.getenv("WEBHOOK_URL")


def main():
    print("Requesting course details from UVM SOC...")
    r = requests.post(UVM_URL, json=BODY, headers=HEADERS, timeout=10)
    r.raise_for_status()

    data = r.json()

    title = data.get("title")
    crn = data.get("crn")
    code = data.get("code")
    print(f"Course: {code} (CRN {crn}) – {title}")

    seats_html = data.get("seats", "")
    print("Seats HTML:", seats_html)

    m = re.search(r"seats_avail[^>]*>(\d+)<", seats_html)
    if not m:
        print("❌ Could not find seats_avail in the response.")
        return

    seats_avail = int(m.group(1))
    print(f"Parsed seats_avail = {seats_avail}")

    # Only trigger when there are actually open seats
    if seats_avail <= 0:
        print("😔 No open seats right now. Not triggering webhook.")
        return

    print("🎉 THERE ARE OPEN SEATS!")

    if not WEBHOOK_URL:
        print("WEBHOOK_URL not set, skipping IFTTT trigger.")
        return

    print("Triggering IFTTT webhook (no payload)...")
    resp = requests.post(WEBHOOK_URL, timeout=10)
    print(f"IFTTT HTTP status: {resp.status_code}")
    print(f"IFTTT response body: {resp.text}")
    resp.raise_for_status()
    print("✅ IFTTT webhook fired successfully.")


if __name__ == "__main__":
    main()
