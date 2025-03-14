from dv_ui import dv_ui

# start on API here

exitValue = False
print(dv_ui(exitValue, 0))
print(dv_ui(exitValue, 1))

API_KEY = "NO_API_KEY_TO_SEE_HERE"
URL = f"https://addressvalidation.googleapis.com/v1:validateAddress?key={API_KEY}"