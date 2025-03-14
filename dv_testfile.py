from dv_ui import dv_ui
import requests 
import os

# Usage of function: addyvally(dv_ui(exitValue, 0)) will return a string value with the validated address

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
URL = f"https://addressvalidation.googleapis.com/v1:validateAddress?key={API_KEY}"

def addyvally(addy):
    payload = {
        "address": {
            "addressLines": addy[0],
            "locality": addy[1],
            "regionCode": "CA"
        }    
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(URL, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        formatted_address = result.get("result", {}).get("address", {}).get("formattedAddress", "No address found")
        print("Validated Address:", formatted_address)
        return formatted_address
    else:
        print("Error:", response.status_code, response.text)
        return None
    
addyvally(dv_ui(0, 0))