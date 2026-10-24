# Obesity & Diabetes Trends

> **An end-to-end ETL pipeline analysing adult obesity and diabetes prevalence across South Africa, the USA, the UK, and Nigeria.**

This project uses data from the **World Health Organization (WHO) Global Health Observatory** to explore how adult obesity and diabetes prevalence have changed over several decades.

The project combines **data engineering, data analysis, and public health context**, drawing on my background as a **dietitian** to investigate significant global health trends through a data-driven approach.

---

## Project Overview

The pipeline extracts obesity and diabetes prevalence data from the WHO Global Health Observatory API, transforms it into analysis-ready datasets, stores them in a local SQLite database, and produces charts comparing trends across four countries.

### Countries analysed

* 🇿🇦 South Africa
* 🇺🇸 United States
* 🇬🇧 United Kingdom
* 🇳🇬 Nigeria

### Time period

* **Obesity:** 1980–2024
* **Diabetes:** 1990–2022

### Health indicators

* **Obesity:** `NCD_BMI_30A`, age-standardized prevalence of obesity among adults (BMI ≥ 30)
* **Diabetes:** `NCD_DIABETES_PREVALENCE_AGESTD`, age-standardized prevalence of diabetes among adults (18+)

---

## ETL Pipeline

```text
             WHO Global Health Observatory API
                          │
          ┌───────────────┴───────────────┐
          ▼                               ▼
 get_obesity_data.py             get_diabetes_data.py
          │                               │
          ▼                               ▼
   obesity_raw.json                diabetes_raw.json
          │                               │
          ▼                               ▼
 clean_obesity_data.py           clean_diabetes_data.py
          │                               │
          ▼                               ▼
   obesity_clean.csv               diabetes_clean.csv
          │                               │
          ▼                               ▼
 save_obesity_data.py            save_diabetes_data.py
          │                               │
          └───────────────┬───────────────┘
                          ▼
                     obesity.db
                    (SQLite)
                          │
          ┌───────────────┴───────────────┐
          ▼                               ▼
 show_obesity_trends.py          show_diabetes_trends.py
          │                               │
          ▼                               ▼
 obesity_trends_chart.png        diabetes_trends_chart.png
```

The project follows an **Extract → Transform → Load → Visualize** workflow for each topic. `run_pipeline.py` runs the steps for one topic, or both.

---

## Pipeline Steps

Each topic has the same four steps.

### 1. Extract

**`get_obesity_data.py`** and **`get_diabetes_data.py`** connect to the WHO Global Health Observatory OData API and save the records for the four countries as `obesity_raw.json` and `diabetes_raw.json`.

### 2. Transform

**`clean_obesity_data.py`** keeps the both-sexes rows for adults and saves `obesity_clean.csv`.

**`clean_diabetes_data.py`** keeps the both-sexes rows for adults aged 18+ and saves `diabetes_clean.csv`.

Both cleaned files have one row per country per year, with these columns:

| Column             | Description                  |
| ------------------ | ---------------------------- |
| `country`          | WHO country code (ZAF, USA, GBR, NGA) |
| `year`             | Year of observation          |
| `obesity_percent` or `diabetes_percent` | Adult prevalence (%) |

### 3. Load

**`save_obesity_data.py`** and **`save_diabetes_data.py`** write each cleaned file into the SQLite database `obesity.db`, as the tables `obesity` and `diabetes`.

This shows how cleaned data can move from a flat-file format into a structured relational database for querying and analysis.

### 4. Visualize

**`show_obesity_trends.py`** queries the `obesity` table with SQL, pivots it by country, and saves `obesity_trends_chart.png`.

**`show_diabetes_trends.py`** does the same for the `diabetes` table and saves `diabetes_trends_chart.png`.

---

## Key Findings

### Obesity (1980–2024)

| Country        | 1980  | 2024  |
| -------------- | ----- | ----- |
| United States  | 12.1% | 41.0% |
| South Africa   | 10.7% | 31.8% |
| United Kingdom | 6.9%  | 27.4% |
| Nigeria        | 1.3%  | 13.7% |

* Adult obesity prevalence rose in all four countries over the period.
* The **USA** had the highest prevalence throughout and the largest absolute increase (about 29 percentage points).
* **South Africa's** prevalence was above the UK's in every year from 1980 to 2024.
* **Nigeria** started from the lowest base but had the fastest relative growth, rising about tenfold.

### Diabetes (1990–2022)

| Country        | 1990  | 2022  |
| -------------- | ----- | ----- |
| United States  | 7.0%  | 12.5% |
| South Africa   | 10.8% | 13.9% |
| United Kingdom | 4.4%  | 8.8%  |
| Nigeria        | 6.2%  | 10.9% |

* **South Africa** had the highest prevalence in both 1990 and 2022, but the smallest increase of the four countries (about 3 percentage points).
* The **United States** had the largest increase (about 5.5 percentage points).
* The **United Kingdom** roughly doubled, from 4.4% to 8.8%.

> *The project describes trends in the available data and does not test causes. The obesity and diabetes series cover different periods, so they are not compared directly.*

---

## How to Run

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd obesity-diabetes-trends
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the pipeline

Run both topics with one command:

```bash
python run_pipeline.py all
```

Or run one topic:

```bash
python run_pipeline.py obesity
python run_pipeline.py diabetes
```

The runner stops and reports the step that failed, if any.

### 4. View the output

The charts are saved as:

```text
obesity_trends_chart.png
diabetes_trends_chart.png
```

### 5. Run the tests

```bash
python -m unittest discover -s tests -v
```

The tests use small fake datasets, so they don't need an internet connection.

---

## Tech Stack

| Technology      | Purpose                          |
| --------------- | -------------------------------- |
| **Python**      | Main programming language        |
| `requests`      | API requests                     |
| `pandas`        | Data cleaning and transformation |
| `sqlite3`       | Local relational database        |
| `matplotlib`    | Data visualization               |
| `unittest`      | Automated tests                  |
| **WHO GHO API** | Source of health data            |

---

## Project Structure

```text
.
├── run_pipeline.py
│
├── get_obesity_data.py
├── clean_obesity_data.py
├── save_obesity_data.py
├── show_obesity_trends.py
│
├── get_diabetes_data.py
├── clean_diabetes_data.py
├── save_diabetes_data.py
├── show_diabetes_trends.py
│
├── tests/
│   ├── helpers.py
│   ├── test_obesity.py
│   ├── test_diabetes.py
│   └── test_run_pipeline.py
│
├── requirements.txt
├── obesity_raw.json
├── obesity_clean.csv
├── diabetes_raw.json
├── diabetes_clean.csv
├── obesity.db           
│
├── obesity_trends_chart.png
├── diabetes_trends_chart.png
│
└── README.md
```

---

## Data Source

**World Health Organization — Global Health Observatory (GHO)**

**Indicator (obesity):** `NCD_BMI_30A`
**Indicator (diabetes):** `NCD_DIABETES_PREVALENCE_AGESTD`

The data is retrieved through the WHO Global Health Observatory OData API.

---

Rather than using an artificial dataset, this project works with real-world public health data and demonstrates a complete data workflow:

```text
API
 ↓
Data Extraction
 ↓
Data Cleaning
 ↓
Relational Database
 ↓
SQL Querying
 ↓
Data Visualization
 ↓
Automated Tests
```
## Verification Code

WTC-J6DAZPTC
