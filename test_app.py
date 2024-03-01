from flask import Flask, render_template, request
import csv
import requests
from datetime import datetime

app = Flask(__name__)

# Function to get the price data for a given symbol and timestamp
def get_price_data(token_symbol, timestamp):
    # Convert timestamp to UNIX timestamp
    unix_timestamp = int(datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').timestamp())

    # Construct the URL dynamically based on the token symbol and UNIX timestamp
    url = f"https://api.coingecko.com/api/v3/coins/{token_symbol.lower()}/market_chart/range?vs_currency=usd&from={unix_timestamp}&to={unix_timestamp + 60}"  # Adding 60 seconds to cover a minute past the hour
    print("URL:", url)  # Print the URL
    headers = {"x-cg-demo-api-key": "CG-dUe4fZZZuifBZehP9835Gm7W"}

    # Send a GET request to the Coingecko API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()  # Parse JSON response
        if 'prices' in data:
            prices = data['prices']
            if prices:
                timestamp, price = prices[0]  # Get the first item in the prices list
                return {'token_symbol': token_symbol, 'timestamp': timestamp, 'price': price}
    return None

# Route for the homepage
@app.route('/')
def index():
    return render_template('Testcsv.html')

# Route to handle file upload and process data
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        data = []
        reader = csv.reader(file)
        header = next(reader)  # Get the header row
        token_symbol_index = header.index('Symbol')  # Find the index of 'Symbol' column
        for i, row in enumerate(reader):
            if i >= 3:
                break
            token_symbol = row[token_symbol_index]
            timestamp = row[0]  # Assuming the timestamp is in the first column
            data.append({'token_symbol': token_symbol, 'timestamp': timestamp})
        
        price_data = []
        for item in data:
            price_data.append(get_price_data(item['token_symbol'], item['timestamp']))
        
        return render_template('Testcsv.html', price_data=price_data)
    return "No file uploaded"

if __name__ == '__main__':
    app.run(debug=True)
