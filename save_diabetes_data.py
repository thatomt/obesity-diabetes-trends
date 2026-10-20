import sqlite3

import pandas as pd


table = pd.read_csv("diabetes_clean.csv")


conn = sqlite3.connect("obesity.db")


table.to_sql("diabetes", conn, if_exists="replace", index=False)


conn.close()

print("Done. Saved into obesity.db, table name: diabetes")