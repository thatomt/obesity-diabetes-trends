# Obesity & Diabetes Trends

> **The pipeline extracts obesity and diabetes prevalence data from the WHO Global Health Observatory API, transforms it into analysis-ready datasets, stores them in a local SQLite database, and produces visualizations comparing trends across four countries.**

This project uses data from the **World Health Organization (WHO) Global Health Observatory** to explore how adult obesity prevalence has changed over more than four decades.

The project combines **data engineering, data analysis, and public health context**, drawing on my background as a **dietitian** to investigate a significant global health trend through a data-driven approach.

---

## Project Overview

The pipeline extracts obesity prevalence data from the WHO Global Health Observatory API, transforms it into an analysis-ready dataset, stores it in a local SQLite database, and produces a visualization comparing trends across four countries.

### Countries analysed

* 🇿🇦 South Africa
* 🇺🇸 United States
* 🇬🇧 United Kingdom
* 🇳🇬 Nigeria

### Time period

* **Obesity:** 1980–2024
* **Diabetes:** 1990–2022

### Health indicator

* **Obesity:** `NCD_BMI_30A`, age-standardized prevalence of obesity among adults (BMI ≥ 30)
* **Diabetes:** `NCD_DIABETES_PREVALENCE_AGESTD`, age-standardized prevalence of diabetes among adults

---

## ETL Pipeline

```text
             WHO Global Health Observatory API
                          │
                          ▼
                 get_obesity_data.py
                          │
                          ▼
                   obesity_raw.json
                          │
                          ▼
                clean_obesity_data.py
                          │
                          ▼
                   obesity_clean.csv
                          │
                          ▼
                 save_obesity_data.py
                          │
                          ▼
                     obesity.db
                    (SQLite)
                          │
                          ▼
               show_obesity_trends.py
                          │
                          ▼
              obesity_trends_chart.png
```

The project follows a simple **Extract → Transform → Load → Visualize** workflow.

---

## Pipeline Steps

### 1. Extract

**`get_obesity_data.py`**

Connects to the WHO Global Health Observatory OData API and retrieves adult obesity prevalence data.

The extraction is filtered to:

* South Africa
* USA
* UK
* Nigeria
* 1980–2024
* Indicator `NCD_BMI_30A`

The raw API response is saved as:

```text
obesity_raw.json
```

---

### 2. Transform

**`clean_obesity_data.py`**

Cleans and prepares the raw WHO data for analysis.

The transformation process:

* Filters the dataset to **both sexes combined**
* Selects the relevant country and year information
* Removes unnecessary fields
* Reshapes the data into an analysis-friendly structure

The resulting dataset contains:

| Column               | Description                  |
| -------------------- | ---------------------------- |
| `country`            | Country name                 |
| `year`               | Year of observation          |
| `obesity_percentage` | Adult obesity prevalence (%) |

Output:

```text
obesity_clean.csv
```

---

### 3. Load

**`save_obesity_data.py`**

Loads the cleaned dataset into a local **SQLite database**.

Output:

```text
obesity.db
```

This demonstrates how cleaned data can move from a flat-file format into a structured relational database for querying and analysis.

---

### 4. Visualize

**`show_obesity_trends.py`**

Queries the SQLite database using SQL and generates a line chart comparing obesity prevalence across all four countries.

Output:

```text
obesity_trends_chart.png
```

The visualization makes it easier to identify long-term changes, differences between countries, and periods of increasing prevalence.

---

### Diabetes pipeline

The same four steps run for diabetes:

* `get_diabetes_data.py` saves `diabetes_raw.json`
* `clean_diabetes_data.py` keeps both sexes and adults 18+, and saves `diabetes_clean.csv`
* `save_diabetes_data.py` writes a `diabetes` table into `obesity.db`
* `show_diabetes_trends.py` saves `diabetes_trends_chart.png`

---

## Key Findings

The data shows a substantial long-term increase in adult obesity prevalence across the countries analysed since 1980.

The trends provide a useful comparison between countries at different stages of the obesity epidemic, while also highlighting the scale and persistence of obesity as a global public health challenge.

**South Africa is particularly important in this analysis**, given the country's changing nutrition landscape and the coexistence of undernutrition and rising overweight and obesity.

> *The project focuses on describing trends in the available data rather than attempting to establish causal relationships.*

### Diabetes (1990–2022)

Age-standardized diabetes prevalence among adults aged 18+:

| Country        | 1990  | 2022  |
| -------------- | ----- | ----- |
| United States  | 7.0%  | 12.5% |
| South Africa   | 10.8% | 13.9% |
| United Kingdom | 4.4%  | 8.8%  |
| Nigeria        | 6.2%  | 10.9% |

* **South Africa** had the highest prevalence in both 1990 and 2022, but the smallest increase of the four countries (about 3 percentage points).
* The **United States** had the largest increase (about 5.5 percentage points).
* The **United Kingdom** roughly doubled, from 4.4% to 8.8%.

> *The diabetes data covers 1990–2022, so it can't be compared directly with the 1980–2024 obesity figures.*

---

## How to Run

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd obesity-diabetes-trends
```

### 2. Install dependencies

```bash
pip install requests pandas matplotlib
```

### 3. Run the ETL pipeline

Run the scripts in order:

```bash
python get_obesity_data.py
python clean_obesity_data.py
python save_obesity_data.py
python show_obesity_trends.py
```

### 4. View the output

The final visualization will be generated as:

```text
obesity_trends_chart.png
```

---

## Tech Stack

| Technology      | Purpose                          |
| --------------- | -------------------------------- |
| **Python**   | Main programming language        |
| `requests`      | API requests                     |
| `pandas`        | Data cleaning and transformation |
| `sqlite3`       | Local relational database        |
| `matplotlib`    | Data visualization               |
| **WHO GHO API** | Source of health data            |

---

## Project Structure

```text
.
├── get_obesity_data.py
├── clean_obesity_data.py
├── save_obesity_data.py
├── show_obesity_trends.py
│
├── obesity_raw.json
├── obesity_clean.csv
├── obesity.db
│
├── obesity_trends_chart.png
│
└── README.md
```

---

## Data Source

**World Health Organization — Global Health Observatory (GHO)**

**Indicator (diabetes):** `NCD_DIABETES_PREVALENCE_AGESTD`

**Indicator:** `NCD_BMI_30A`

**Description:** Age-standardized prevalence of obesity among adults (BMI ≥ 30).

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
```
## Verification Code

WTC-J6DAZPTC
