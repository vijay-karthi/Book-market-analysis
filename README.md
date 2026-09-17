# Book Market Analysis

A small end-to-end data analysis project that scrapes book information from Books to Scrape, cleans it, stores it in SQLite, runs SQL queries, and exports the results for further analysis.

This project follows the full workflow:

Web Scraping → Data Cleaning → SQLite → SQL Analysis → Excel Export

---

## Overview

The project gathers book listings from a public sample e-commerce site and analyzes:

- price distribution
- category distribution
- average price by category
- average rating by category
- high-price and low-rating combinations
- top and bottom-priced books

The core objective is to turn raw scraped data into a structured dataset and answer business-oriented questions with SQL.

---

## Tech Stack

- Python
- pandas
- requests
- BeautifulSoup4
- SQLite
- openpyxl
- SQL

---

## Project Structure

```text
book-market-analysis/
├── analysis/
│   └── clean_data.py
├── dashboard/
├── data/
│   ├── processed/
│   │   └── books_clean.csv
│   └── raw/
│       └── books_raw.csv
├── scraper/
│   └── scraper.py
├── sql/
│   ├── analysis.sql
│   ├── database.py
│   └── run_queries.py
├── .gitignore
├── README.md
├── requirements.txt
└──
```

---

## Data Pipeline

### 1. Web Scraping

The scraper in [scraper/scraper.py](scraper/scraper.py) crawls the Books to Scrape website and collects:

- title
- price
- rating
- availability
- category
- product URL
- scraped date

Raw data is saved to:

- [data/raw/books_raw.csv](data/raw/books_raw.csv)

### 2. Data Cleaning

The cleaning script in [analysis/clean_data.py](analysis/clean_data.py) standardizes the data by:

- removing currency symbols from prices
- converting price values to numeric values
- mapping rating text to numeric values
- filling missing categories as Unknown
- converting scraped dates to datetime format
- removing duplicate product URLs
- dropping the availability column if it has no analytical value
- filling missing numeric values safely

Cleaned data is saved to:

- [data/processed/books_clean.csv](data/processed/books_clean.csv)

### 3. SQLite Database

The script in [sql/database.py](sql/database.py) loads the cleaned CSV into a SQLite database and creates the `books` table.

Database output:

- [data/books.db](data/books.db)

### 4. SQL Analysis

The SQL queries in [sql/analysis.sql](sql/analysis.sql) answer questions such as:

- total books and market summary
- books per category
- average price by category
- average rating by category
- most expensive and cheapest books
- high-price / low-rating books
- price distribution by rating
- categories with more than 20 books

### 5. Excel Export

The script in [sql/run_queries.py](sql/run_queries.py) runs all queries, saves the results to a SQLite database, and exports them to Excel as multiple sheets.

Output:

- [dashboard/SQL Results.xlsx](dashboard/SQL Results.xlsx)

---

## Setup

1. Clone the repository

```bash
git clone <repository-url>
cd book-market-analysis
```

2. Create and activate a virtual environment (optional but recommended)

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Project

### Step 1: Scrape the data

```bash
python scraper/scraper.py
```

This creates the raw dataset in [data/raw/books_raw.csv](data/raw/books_raw.csv).

### Step 2: Clean the data

```bash
python analysis/clean_data.py
```

This creates the processed dataset in [data/processed/books_clean.csv](data/processed/books_clean.csv).

### Step 3: Create the SQLite database

```bash
python sql/database.py
```

This creates the database file in [data/books.db](data/books.db).

### Step 4: Run SQL analysis and export to Excel

```bash
python sql/run_queries.py
```

This creates the Excel workbook in [dashboard/SQL Results.xlsx](dashboard/SQL Results.xlsx).

---

## Requirements

The project dependencies are listed in [requirements.txt](requirements.txt):

- requests
- beautifulsoup4
- pandas
- matplotlib
- openpyxl

---

## Notes

- The project is designed as a portfolio-style data analytics workflow.
- The dataset is sourced from a sample bookstore site used for educational scraping practice.
- If the database or Excel output is missing, rerun the earlier steps in order.

---

## Future Improvements

Possible extensions for this project include:

- building a more polished dashboard in Power BI or Excel
- adding more analysis questions and KPIs
- adding automated validation checks for scraped data
- publishing the project as a reproducible notebook or pipeline

Nonfiction is the largest identified category with 108 books, while 210 books are classified as Unknown.

Price Differences

Among categories with at least 10 books, Travel has the highest average listed price at £41.17, while Thriller averages £31.43.

Ratings & Price

Average listed price varies only modestly across ratings, ranging from £34.50 for 1-star books to £35.88 for 4-star books.

High-Price, Low-Rating

The dataset contains books priced at £50 or more with ratings of 1–2 stars, showing that higher listed prices do not necessarily correspond to higher ratings.

⚠️ Limitations
The dataset represents book listings collected from the website, not actual sales or revenue.
Listed prices should not be interpreted as actual transaction prices.
Ratings are displayed on a 1–5 scale.
Some category values were unavailable or unreliable and were grouped under Unknown.
The analysis represents a snapshot of the website rather than historical price changes.
The dataset does not contain sales volume, revenue, customer demographics, or purchase behavior.
🎯 Project Objective

The main objective of this project is to demonstrate the ability to transform raw web data into structured, business-oriented insights.

The workflow covers:

Data Collection → Data Cleaning → Data Storage → SQL Analysis → Data Visualization → Business Insights

👨‍💻 Skills Demonstrated
Web Scraping
Data Cleaning
Data Transformation
Exploratory Data Analysis
SQL
SQLite
Pandas
Excel Dashboarding
Data Visualization
Business Analysis
Git & GitHub
Project Documentation
📌 Conclusion

This project demonstrates an end-to-end Data Analyst workflow using Python, SQL, SQLite, and Excel.

Starting with raw e-commerce data, the project cleans and structures the data, stores it in a relational database, performs SQL-based analysis, and presents the results through an interactive Excel dashboard.

The project provides practical experience in turning raw data into meaningful business insights.