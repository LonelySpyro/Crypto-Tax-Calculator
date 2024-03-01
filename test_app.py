from flask import Flask, render_template, request
import csv
import requests
from datetime import datetime

app = Flask(__name__)

def fetch_coin_id(symbol):
    url = f"https://api.coingecko.com/api/v3/coins/list"
    headers = {"x-cg-api-key": "CG-dUe4fZZZuifBZehP9835Gm7W"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        coin_list = response.json()
        for coin in coin_list:
            if coin["symbol"].lower() == symbol.lower():
                return coin["id"]
    return None

def process_csv(content):
    csv_reader = csv.reader(content.split('\n'))
    data = list(csv_reader)
    for row in data:
        symbol = row[5]  # Assuming the symbol is in the 6th column (0-indexed)
        coin_id = fetch_coin_id(symbol)
        if coin_id:
            row[5] = coin_id
        else:
            print(f"Could not find ID for symbol: {symbol}")
    return data

def get_price_data(coin_id, timestamp):
    unix_timestamp = int(datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').timestamp())
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range?vs_currency=usd&from={unix_timestamp}&to={unix_timestamp + 60}"  # Adding 60 seconds to cover a minute past the hour
    headers = {"x-cg-demo-api-key": "CG-dUe4fZZZuifBZehP9835Gm7W"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if 'prices' in data:
            prices = data['prices']
            if prices:
                timestamp, price = prices[0]
                return {'coin_id': coin_id, 'timestamp': timestamp, 'price': price}
    return None

@app.route('/')
def index():
    return render_template('Testcsv.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        content = file.read().decode('utf-8')
        data = process_csv(content)
        price_data = []
        for row in data[1:4]:  # Assuming you want to process only first 3 rows
            timestamp = row[0]  # Assuming timestamp is in the first column
            coin_id = row[5]  # Assuming ID is in the 6th column
            price_data.append(get_price_data(coin_id, timestamp))
        return render_template('Testcsv.html', price_data=price_data)
    return "No file uploaded"

if __name__ == '__main__':
    app.run(debug=True)
