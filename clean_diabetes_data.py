import json
import pandas as pd

with open("diabetes_raw.json", "r") as f:
    records = json.load(f)


adults = [
    r for r in records
    if r["Dim1"] == "SEX_BTSX" and r["Dim2"] == "AGEGROUP_YEARS18-PLUS"
]


table = pd.DataFrame([
    {
        "country": r["SpatialDim"],
        "year": r["TimeDim"],
        "diabetes_percent": r["NumericValue"],
    }
    for r in adults
])

table = table.sort_values(["country", "year"])
table.to_csv("diabetes_clean.csv", index=False)
print(f"Saved {len(table)} rows to diabetes_clean.csv")