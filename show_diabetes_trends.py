import sqlite3

import matplotlib.pyplot as plt
import pandas as pd


conn = sqlite3.connect("obesity.db")
df = pd.read_sql_query("SELECT country, year, diabetes_percent FROM diabetes", conn)
conn.close()


table = df.pivot(index="year", columns="country", values="diabetes_percent")


table.plot(figsize=(10, 6), marker="o", markersize=3)
plt.title("Adult Diabetes Prevalence (age-standardized, 18+), 1990-2022")
plt.xlabel("Year")
plt.ylabel("Diabetes prevalence (%)")
plt.grid(True, alpha=0.3)
plt.legend(title="Country")
plt.tight_layout()


plt.savefig("diabetes_trends_chart.png", dpi=150)
print("Saved diabetes_trends_chart.png")