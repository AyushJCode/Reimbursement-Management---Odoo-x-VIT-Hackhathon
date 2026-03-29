import requests

def convert_currency(amount, from_currency, to_currency):
    """
    Converts an amount from one currency to another using ExchangeRate-API.
    """
    if from_currency == to_currency:
        return amount
    
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url)
        data = response.json()
        
        exchange_rate = data['rates'][to_currency]
        return round(amount * exchange_rate, 2)
    except Exception as e:
        print(f"Error converting currency: {e}")
        # Return original amount as fallback or handle error as needed
        return amount