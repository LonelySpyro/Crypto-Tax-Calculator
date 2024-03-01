import requests

url = "https://api.coingecko.com/api/v3/coins/list"

headers = {"x-cg-api-key": "CG-dUe4fZZZuifBZehP9835Gm7W"}

response = requests.get(url, headers=headers)

print(response.text)