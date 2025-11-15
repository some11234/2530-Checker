import re
import requests

# UVM SOC API endpoint
UVM_URL = "https://soc.uvm.edu/api/?page=fose&route=details"

# Body for HLTH 2530, CRN 14157, term 202601
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

def main():
    print("Requesting course details from UVM SOC...")
    r = requests.post(UVM_URL, json=BODY, headers=HEADERS, timeout=10)
    r.raise_for_status()

    data = r.json()

    # Just to sanity check:
    title = data.get("title")
    crn = data.get("crn")
    code = data.get("code")
    print(f"Course: {code} (CRN {crn}) – {title}")

    # The seats HTML looks like:
    # "seats":"... <span class=\"seats_avail\">0</span>"
    seats_html = data.get("seats", "")
    print("Seats HTML:", seats_html)

    m = re.search(r"seats_avail[^>]*>(\d+)<", seats_html)
    if not m:
        print("Could not find seats_avail in the response.")
        return

    seats_avail = int(m.group(1))
    print(f"✅ Parsed seats_avail = {seats_avail}")

    if seats_avail > 0:
        print("🎉 THERE ARE OPEN SEATS!")
    else:
        print("😔 No open seats right now.")

if __name__ == "__main__":
    main()
