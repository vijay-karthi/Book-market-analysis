from pathlib import Path
import pandas as pd


# =========================
# PROJECT PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_PATH = BASE_DIR / "data" / "raw" / "books_raw.csv"
CLEAN_PATH = BASE_DIR / "data" / "processed" / "books_clean.csv"


# =========================
# LOAD RAW DATA
# =========================

df = pd.read_csv(RAW_PATH)

print("\n===== RAW DATA =====")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")


# =========================
# CLEAN PRICE
# =========================

df["price"] = (
    df["price"]
    .str.replace("Â£", "", regex=False)
    .str.replace("£", "", regex=False)
    .str.strip()
)

df["price"] = pd.to_numeric(
    df["price"],
    errors="coerce"
)


# =========================
# CLEAN RATING
# =========================

rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

df["rating"] = df["rating"].map(rating_map)


# =========================
# CLEAN CATEGORY
# =========================

df["category"] = df["category"].fillna("Unknown")


# =========================
# CLEAN DATE
# =========================

df["scraped_date"] = pd.to_datetime(
    df["scraped_date"],
    errors="coerce"
)


# =========================
# REMOVE DUPLICATES
# =========================

before = len(df)

df = df.drop_duplicates(
    subset="product_url"
)

after = len(df)

print("\n===== DUPLICATES =====")
print(f"Removed: {before - after}")


# =========================
# REMOVE AVAILABILITY
# =========================

# The source contains only "In stock"
# for all books, so it does not provide
# useful analytical information.

df = df.drop(columns=["availability"])


# =========================
# HANDLE MISSING VALUES
# =========================

print("\n===== MISSING VALUES BEFORE CLEANING =====")
print(df.isnull().sum())


# Clean category values
# "Default" and "Add a comment" are breadcrumb artifacts
df["category"] = df["category"].replace(
    ["Default", "Add a comment"],
    "Unknown"
)

df["category"] = df["category"].fillna("Unknown")


# Use median for numeric fields if
# unexpected missing values exist.
df["price"] = df["price"].fillna(
    df["price"].median()
)

df["rating"] = df["rating"].fillna(
    df["rating"].median()
)


# =========================
# VALIDATION
# =========================

print("\n===== CLEAN DATA =====")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== MISSING VALUES AFTER CLEANING =====")
print(df.isnull().sum())

print("\n===== FIRST 5 CLEAN ROWS =====")
print(df.head())


# =========================
# SAVE CLEAN DATA
# =========================

CLEAN_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    CLEAN_PATH,
    index=False
)


print("\n===== CLEANING COMPLETE =====")
print(f"Clean file saved to: {CLEAN_PATH}")