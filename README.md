# Obesity & Diabetes Trends

An ETL pipeline that pulls WHO obesity prevalence data (1980-2024) for South Africa, the USA, UK, and Nigeria and visualizes how rates have changed over more than four decades.

Built to explore a genuinely important public health trend, combining data engineering with professional dietitian background.

How it works
WHO GHO API → get_obesity_data.py → obesity_raw.json
                                            |
                                            v
                clean_obesity_data.py → obesity_clean.csv
                                            |
                                            v
                 save_obesity_data.py → obesity.db (SQLite)
                                            |
                                            v
                show_obesity_trends.py → obesity_trends_chart.png
Steps
Extract (get_obesity_data.py) — downloads adult obesity prevalence data (indicator NCD_BMI_30A) from the WHO Global Health Observatory API, filtered to South Africa, USA, UK, and Nigeria.
Transform (clean_obesity_data.py) — filters to "both sexes combined" rows and reshapes into a clean table: country, year, obesity percentage.
Load (save_obesity_data.py) — loads the clean table into a local SQLite database.
Serve (show_obesity_trends.py) — queries the database and charts obesity trends for all 4 countries on one graph.
