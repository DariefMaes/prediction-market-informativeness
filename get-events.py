import requests
import time
import json

BASE_URL = "https://api.elections.kalshi.com/trade-api/v2/events"

def fetch_events(n=10000):
    all_events = []
    cursor = None

    while len(all_events) < n:
        params = {
            "limit": 200,
            "status": "settled"
        }
        if cursor:
            params["cursor"] = cursor

        r = requests.get(BASE_URL, params=params)
        data = r.json()

        batch = data.get("events", [])
        all_events.extend(batch)

        cursor = data.get("cursor")

        print(f"Fetched {len(all_events)} events so far…")

        if not cursor:
            break

        time.sleep(0.25)

    return all_events

events = fetch_events(10000)

with open("events.json", "w") as f:
    json.dump(events, f)
