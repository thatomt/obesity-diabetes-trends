import json
import pandas as pd

with open("obesity_raw.json", "r") as f:
    records = json.load(f)

both_sexes = [r for r in records if r["Dim1"] == "SEX_BTSX"]

table = pd.DataFrame([
    {
        "country": r["SpatialDim"],
        "year": r["TimeDim"],
        "obesity_percent": r["NumericValue"],
    }
    for r in both_sexes
])

table = table.sort_values(["country", "year"])
table.to_csv("obesity_clean.csv", index=False)
print(f"Saved {len(table)} rows to obesity_clean.csv")