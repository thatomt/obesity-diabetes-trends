import requests
import json

# WHO indicator code for age-standardized adult obesity prevalence
INDICATOR = "NCD_BMI_30A"

# Countries to compare (ISO-3 codes)
# ZAF = South Africa, USA = United States, GBR = UK, NGA = Nigeria
COUNTRIES = ["ZAF", "USA", "GBR", "NGA"]

url = f"https://ghoapi.azureedge.net/api/{INDICATOR}"

print("Downloading WHO obesity data...")
response = requests.get(url)
data = response.json()


all_records = data["value"]
filtered_records = [
    record for record in all_records
    if record.get("SpatialDim") in COUNTRIES
]

print(f"Downloaded {len(all_records)} total records, kept {len(filtered_records)} for our countries.")

with open("obesity_raw.json", "w") as f:
    json.dump(filtered_records, f, indent=2)

print("Done. Saved to obesity_raw.json")