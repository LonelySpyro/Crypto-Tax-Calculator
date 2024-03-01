import requests
from datetime import datetime

url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from=1672531200&to=1672617600"

headers = {"x-cg-demo-api-key": "CG-dUe4fZZZuifBZehP9835Gm7W"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()  # Parse JSON response

    if 'prices' in data:
        prices = data['prices']
        for timestamp, price in prices:
            readable_time = datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
        print("Time:", readable_time, "Price", price)
    else:
        print("Current price not found")

