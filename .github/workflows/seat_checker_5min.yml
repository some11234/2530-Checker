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
    "X-Requested-With": "XMLHttpRequest"
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

    # 🔥 TEMP: force trigger when seats_avail == 0 so we can test IFTTT
    if seats_avail == 0:
        print("Test condition met: seats_avail == 0, should trigger webhook.")
    else:
        print("Test condition NOT met, but we'll still trigger for debugging.")

    print(f"WEBHOOK_URL present? {'yes' if WEBHOOK_URL else 'NO'}")

    if not WEBHOOK_URL:
        print("WEBHOOK_URL not set, cannot trigger IFTTT.")
        return

    print("Triggering IFTTT webhook...")
    payload = {
        "value1": "HLTH 2530 EMT (test)",
        "value2": f"CRN {crn}",
        "value3": f"Seats available: {seats_avail}"
    }

    resp = requests.post(WEBHOOK_URL, json=payload, timeout=10)
    print(f"IFTTT HTTP status: {resp.status_code}")
    print(f"IFTTT response body: {resp.text}")

    resp.raise_for_status()
    print("✅ IFTTT webhook fired successfully.")


if __name__ == "__main__":
    main()
