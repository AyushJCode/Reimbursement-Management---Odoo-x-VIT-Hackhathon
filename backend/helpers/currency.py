import requests

def convert_currency(amount, from_currency, to_currency):
    """
    Converts an amount using ExchangeRate-API with a local fallback.
    """
    # 1. Immediate return if currencies match
    if from_currency == to_currency:
        return amount
    
    # 2. Try the Live API
    try:
        # Use a timeout (2 seconds) so the app doesn't freeze if the API is slow
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url, timeout=2)
        response.raise_for_status() # Check if the request was successful
        data = response.json()
        
        exchange_rate = data['rates'].get(to_currency)
        if exchange_rate:
            return round(amount * exchange_rate, 2)
            
    except Exception as e:
        print(f"⚠️ Live Currency API failed: {e}. Using fallback rates.")

    # 3. 🛡️ HARDCODED FALLBACK (Saves your demo if the internet dies)
    # Common rates relative to 1 unit of from_currency (Approximate)
    fallbacks = {
        "USD": {"INR": 83.0, "EUR": 0.92},
        "EUR": {"INR": 90.0, "USD": 1.08},
        "INR": {"USD": 0.012, "EUR": 0.011}
    }
    
    try:
        rate = fallbacks.get(from_currency, {}).get(to_currency)
        if rate:
            return round(amount * rate, 2)
    except:
        pass

    # 4. Absolute Fallback: Return original amount if all else fails
    return amount