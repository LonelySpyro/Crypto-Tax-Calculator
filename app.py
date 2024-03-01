from flask import Flask, render_template, request
import requests
import datetime
import os
from config import API_KEY

app = Flask(__name__)
api_key = os.environ.get('API_KEY')

# Fetch token price at a specific timestamp from CoinGecko
def get_token_price_at_timestamp(token_symbol, timestamp):
    # Convert timestamp to UNIX timestamp
    unix_timestamp = int(timestamp.timestamp())
    
    # Construct the API URL
    url = f'https://api.coingecko.com/api/v3/coins?ids={token_symbol.lower()}bitcoin/history?date={unix_timestamp}'
    
    # Make the API request
    response = requests.get(url)
    
    # Parse the response and extract the price
    if response.status_code == 200:
        data = response.json()
        price = data.get(token_symbol.lower(), {}).get('usd')
        return price
    else:
        # Handle API request error
        return None

# Route for the homepage
@app.route('/')
def index():
    # Render the homepage template
    return render_template('index.html')

# Route to handle form submission and fetch token price
@app.route('/get_price', methods=['POST'])
def get_price():
    # Extract token symbol and timestamp from form data
    token_symbol = request.form['token_symbol']
    timestamp = datetime.datetime.strptime(request.form['timestamp'], '%Y-%m-%d %H:%M:%S')
    
    # Call function to fetch token price
    price = get_token_price_at_timestamp(token_symbol, timestamp)
    
    # Render the result template with token symbol, timestamp, and price
    return render_template('result.html', token_symbol=token_symbol, timestamp=timestamp, price=price)

def calculate_total(token_amount, price):
    return token_amount * price

# Example usage
token_amount = 100
price = 50.25  # Assuming the price per token is $50.25
total_value = calculate_total(token_amount, price)
print("Total value:", total_value)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
