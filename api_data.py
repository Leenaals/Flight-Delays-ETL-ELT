import requests
import pandas as pd

# API link
url = "https://api.aviationstack.com/v1/flights"


params = {
    "access_key": "YOUR_API_KEY_HERE",
    "limit": 5
}


response = requests.get(url, params=params)
data = response.json()


if "data" in data:
    df = pd.json_normalize(data["data"])
    
    
    df.to_csv("api_flights.csv", index=False)
    print("API data saved ✅")
else:
    print("Error in API")