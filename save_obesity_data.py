import pandas as pd
import sqlite3


table = pd.read_csv("obesity_clean.csv")

# Connect to a database file
conn = sqlite3.connect("obesity.db")

# Save the table into the database, into a table called "obesity"
table.to_sql("obesity", conn, if_exists="replace", index=False)

conn.close()

print("Done. Saved into obesity.db, table name: obesity")