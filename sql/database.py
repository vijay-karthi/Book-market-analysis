from pathlib import Path
import sqlite3
import pandas as pd


# =========================
# PROJECT PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

CLEAN_PATH = BASE_DIR / "data" / "processed" / "books_clean.csv"
DB_PATH = BASE_DIR / "data" / "books.db"


# =========================
# LOAD CLEAN DATA
# =========================

df = pd.read_csv(CLEAN_PATH)

print("\n===== CLEAN DATA LOADED =====")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")


# =========================
# CREATE DATABASE
# =========================

DB_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

connection = sqlite3.connect(DB_PATH)


# =========================
# CREATE BOOKS TABLE
# =========================

df.to_sql(
    "books",
    connection,
    if_exists="replace",
    index=False
)


# =========================
# VERIFY DATABASE
# =========================

cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM books")

row_count = cursor.fetchone()[0]

print("\n===== DATABASE CREATED =====")
print(f"Database: {DB_PATH}")
print(f"Books in database: {row_count}")


# =========================
# SHOW TABLE STRUCTURE
# =========================

cursor.execute("PRAGMA table_info(books)")

columns = cursor.fetchall()

print("\n===== TABLE COLUMNS =====")

for column in columns:
    print(f"- {column[1]} ({column[2]})")


# =========================
# CLOSE DATABASE
# =========================

connection.close()

print("\n===== COMPLETE =====")
print("SQLite database is ready for SQL analysis.")