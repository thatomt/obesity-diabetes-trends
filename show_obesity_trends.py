import sqlite3

import matplotlib.pyplot as plt
import pandas as pd

# read the table from the database with SQL
conn = sqlite3.connect("obesity.db")
df = pd.read_sql_query("SELECT country, year, obesity_percent FROM obesity", conn)
conn.close()

# reshape so each country is its own column, indexed by year
table = df.pivot(index="year", columns="country", values="obesity_percent")

# plot one line per country
table.plot(figsize=(10, 6), marker="o", markersize=3)
plt.title("Adult Obesity Prevalence (BMI >= 30), 1980-2024")
plt.xlabel("Year")
plt.ylabel("Obesity prevalence (%)")
plt.grid(True, alpha=0.3)
plt.legend(title="Country")
plt.tight_layout()

# save the chart as an image
plt.savefig("obesity_trends_chart.png", dpi=150)
print("Saved obesity_trends_chart.png")