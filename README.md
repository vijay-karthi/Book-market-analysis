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

🔄 Data Pipeline
1. Web Scraping

Python is used to collect book information from Books to Scrape.

The scraper collects:

Book title
Price
Rating
Availability
Product URL
Category
Scraped date

The raw dataset is saved to:

data/raw/books_raw.csv

The scraper also visits individual product pages to retrieve category information.

2. Data Cleaning

The raw dataset is cleaned using Pandas.

Cleaning steps include:

Removing currency symbols from prices
Converting prices to numeric values
Converting rating words into numerical ratings
Handling missing categories
Replacing unreliable category values with Unknown
Converting the scraped date into a date format
Removing duplicate product URLs
Removing the availability field because it contained no useful variation
Handling unexpected missing numeric values

The cleaned dataset is saved to:

data/processed/books_clean.csv
3. SQLite Database

The cleaned dataset is loaded into a SQLite database.

Database:

data/books.db

Table:

books

SQLite provides the structured data source for the SQL analysis.

4. SQL Analysis

SQL queries are used to answer business-oriented questions about the dataset.

The analysis includes:

Overall market statistics
Book count by category
Average price by category
Average rating by category
Highest-priced books
Lowest-priced books
Expensive books with low ratings
Average price by rating
Categories containing more than 20 books
Highest-rated books with the highest prices

The SQL queries are stored in:

sql/analysis.sql

The query results are also exported automatically to Excel using:

sql/run_queries.py
📈 Key Findings
Overall Market
920 books were analyzed.
Average listed price: £34.97
Minimum listed price: £10.00
Maximum listed price: £59.99
Average rating: 2.92 / 5
Category Distribution

Nonfiction is the largest identified category with 108 books.

There are also 210 books classified as Unknown, primarily because category information was unavailable or unreliable for those records.

Average Price by Category

Among categories with at least 10 books:

Travel has the highest average listed price at £41.17.
Thriller has an average listed price of £31.43.
Ratings and Price

Average listed price varies only modestly across rating groups:

Rating	Average Price
1 Star	£34.50
2 Stars	£34.55
3 Stars	£34.73
4 Stars	£35.88
5 Stars	£35.36

The dataset therefore does not show a large difference in average listed price across rating groups.

High-Price, Low-Rating Books

The dataset contains books priced at £50 or more with ratings of 1–2 stars.

This indicates that higher listed prices do not necessarily correspond to higher ratings within this dataset.

📊 Excel Dashboard

The final Excel dashboard presents:

Total number of books
Average price
Average rating
Maximum price
Books by category
Average price by category
Average rating by category
Average price by rating
Key business insights

The dashboard and SQL results are available in:

dashboard/SQL Results.xlsx
▶️ How to Run the Project
1. Clone the Repository
git clone https://github.com/vijay-karthi/Book-market-analysis.git
cd Book-market-analysis
2. Install Dependencies
pip install -r requirements.txt
3. Run the Scraper
python scraper/scraper.py

This creates:

data/raw/books_raw.csv
4. Clean the Data
python analysis/clean_data.py

This creates:

data/processed/books_clean.csv
5. Create the SQLite Database
python sql/database.py

This creates:

data/books.db
6. Run SQL Analysis
python sql/run_queries.py

This executes the SQL analysis and exports the results to:

dashboard/SQL Results.xlsx
💡 Business Insights
Category Concentration

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