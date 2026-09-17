# Book Market Analysis

An end-to-end Data Analyst portfolio project analyzing book prices, ratings, and categories from an e-commerce website.

The project demonstrates a complete data analytics workflow:

**Web Scraping → Data Cleaning → SQLite → SQL Analysis → Excel Dashboard → Business Insights**

---

## Project Overview

This project analyzes book listings collected from Books to Scrape.

The goal is to understand:

- Book price distribution
- Category distribution
- Average price by category
- Average rating by category
- Relationship between price and rating
- High-priced books with low ratings
- Highest- and lowest-priced books

The final results are presented through an Excel dashboard.

---

## Dataset

The dataset contains **920 book listings** collected from the website.

The raw dataset includes:

- Book title
- Price
- Rating
- Availability
- Product URL
- Category
- Scraped date

After cleaning, the dataset contains:

- Book title
- Price
- Rating
- Product URL
- Category
- Scraped date

The availability field was removed during cleaning because all collected records had the same availability value and did not provide useful analytical information.

---

## Project Structure

```text
book-market-analysis/
│
├── data/
│   ├── raw/
│   │   └── books_raw.csv
│   ├── processed/
│   │   └── books_clean.csv
│   └── books.db
│
├── scraper/
│   └── scraper.py
│
├── analysis/
│   └── clean_data.py
│
├── sql/
│   ├── analysis.sql
│   ├── database.py
│   └── run_queries.py
│
├── dashboard/
│   └── SQL Results.xlsx
│
├── requirements.txt
├── README.md
└── .gitignore