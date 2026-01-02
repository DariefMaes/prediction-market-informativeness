import json
import pandas as pd
import requests
import time
import numpy as np

# Load events from the file
with open("events.json", "r") as f:
    all_events = json.load(f)

print("Loaded", len(all_events), "events")

chosen_markets = []

for i, event in enumerate(all_events):

    event_ticker = event.get('event_ticker')
    series_ticker = event.get('series_ticker')
    category = event.get('category')

    # Fetch event details
    url = f"https://api.elections.kalshi.com/trade-api/v2/events/{event_ticker}"
    time.sleep(0.15)
    data = requests.get(url).json()

    markets = data.get("markets", [])
    if len(markets) == 0:
        continue

    # Pick highest-volume market
    market = max(markets, key=lambda m: m.get("volume", 0))

    # Skip invalid close_time
    closed = market.get("close_time", "")
    if closed.startswith("0001") or closed is None:
        continue

    closed_dt = pd.to_datetime(closed, utc=True)

    ticker = market["ticker"]

    # Build times
    start_ts_dt = closed_dt - pd.Timedelta(days=30)
    start_ts = int(start_ts_dt.timestamp())
    end_ts   = int(closed_dt.timestamp())

    url = f"https://api.elections.kalshi.com/trade-api/v2/series/{series_ticker}/markets/{ticker}/candlesticks?start_ts={start_ts}&end_ts={end_ts}&period_interval=60"
    
    response = requests.get(url).json()

    if "candlesticks" not in response:
        continue

    candles = response["candlesticks"]
    if len(candles) == 0:
        continue

    # Append each candle
    for candle in candles:
        yes_ask = candle['yes_ask']['open']
        yes_bid = candle['yes_bid']['open']
        price = (yes_ask + yes_bid) / 2

        candle_dt = pd.to_datetime(candle['end_period_ts'], unit='s', utc=True)
        time_until_hours = np.floor((closed_dt - candle_dt).total_seconds() / 3600)

        chosen_markets.append({
            "yes_ask": yes_ask,
            "yes_bid": yes_bid,
            "price": price,
            "result": market.get("result"),
            "close_time": closed,
            "event_ticker": event_ticker,
            "series_ticker": series_ticker,
            "time_until": time_until_hours,
            "ticker": ticker,
            "category": category,
            "volume": market.get("volume", 0),
            "timestamp": candle_dt
        })

    if i % 100 == 0:
        print(f"Handled {i}/{len(all_events)} events ({i/len(all_events)*100:.2f}%)")


print("Total chosen market candles:", len(chosen_markets))
# Save to JSON using Pandas
df = pd.DataFrame(chosen_markets)
df.to_json("chosen_markets.json", orient="records", date_format="iso")
print("Saved chosen markets to chosen_markets.json")