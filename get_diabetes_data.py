import json

import requests

# WHO indicator code for age-standardized diabetes prevalence
INDICATOR = "NCD_DIABETES_PREVALENCE_AGESTD"

# Countries to compare 
COUNTRIES = ["ZAF", "USA", "GBR", "NGA"]

url = f"https://ghoapi.azureedge.net/api/{INDICATOR}"


print("Downloading WHO diabetes data...")
response = requests.get(url)
data = response.json()


all_records = data["value"]
filtered_records = [
    record for record in all_records
    if record.get("SpatialDim") in COUNTRIES
]

print(f"Downloaded {len(all_records)} total records, kept {len(filtered_records)} for our countries.")

with open("diabetes_raw.json", "w") as f:
    json.dump(filtered_records, f, indent=2)

print("Done. Saved to diabetes_raw.json")