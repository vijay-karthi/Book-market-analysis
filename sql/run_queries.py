from pathlib import Path
import sqlite3
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "books.db"
OUTPUT_DIR = BASE_DIR / "dashboard"
OUTPUT_FILE = OUTPUT_DIR / "SQL Results.xlsx"


# ============================================================
# SQL QUERIES
# ============================================================

queries = {

    "Overall Market": """
        SELECT
            COUNT(*) AS total_books,
            ROUND(AVG(price), 2) AS avg_price,
            MIN(price) AS min_price,
            MAX(price) AS max_price,
            ROUND(AVG(rating), 2) AS avg_rating
        FROM books;
    """,

    "Books by Category": """
        SELECT
            category,
            COUNT(*) AS book_count
        FROM books
        GROUP BY category
        ORDER BY book_count DESC;
    """,

    "Avg Price Category": """
        SELECT
            category,
            COUNT(*) AS book_count,
            ROUND(AVG(price), 2) AS avg_price
        FROM books
        GROUP BY category
        HAVING COUNT(*) >= 10
        ORDER BY avg_price DESC;
    """,

    "Avg Rating Category": """
        SELECT
            category,
            COUNT(*) AS book_count,
            ROUND(AVG(rating), 2) AS avg_rating
        FROM books
        GROUP BY category
        HAVING COUNT(*) >= 10
        ORDER BY avg_rating DESC;
    """,

    "Top Expensive": """
        SELECT
            title,
            category,
            price,
            rating
        FROM books
        ORDER BY price DESC
        LIMIT 10;
    """,

    "Top Cheapest": """
        SELECT
            title,
            category,
            price,
            rating
        FROM books
        ORDER BY price ASC
        LIMIT 10;
    """,

    "Expensive Low Rated": """
        SELECT
            title,
            category,
            price,
            rating
        FROM books
        WHERE price >= 50
          AND rating <= 2
        ORDER BY price DESC;
    """,

    "Price by Rating": """
        SELECT
            rating,
            COUNT(*) AS book_count,
            ROUND(AVG(price), 2) AS avg_price,
            MIN(price) AS min_price,
            MAX(price) AS max_price
        FROM books
        GROUP BY rating
        ORDER BY rating;
    """,

    "Categories >20": """
        SELECT
            category,
            COUNT(*) AS book_count,
            ROUND(AVG(price), 2) AS avg_price,
            ROUND(AVG(rating), 2) AS avg_rating
        FROM books
        GROUP BY category
        HAVING COUNT(*) > 20
        ORDER BY book_count DESC;
    """,

    "Highest Rated": """
        SELECT
            title,
            category,
            price
        FROM books
        WHERE rating = 5
        ORDER BY price DESC
        LIMIT 10;
    """
}


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n========================================")
    print("       BOOK MARKET SQL ANALYSIS")
    print("========================================")

    # Check database
    if not DB_PATH.exists():
        print(f"\n[ERROR] Database not found:")
        print(DB_PATH)
        print("\nRun this first:")
        print("python sql/database.py")
        return

    # Create dashboard directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Connect to SQLite
    connection = sqlite3.connect(DB_PATH)

    # Store query results
    results = {}

    print("\nRunning SQL queries...\n")

    for sheet_name, query in queries.items():

        df = pd.read_sql_query(query, connection)

        results[sheet_name] = df

        print(f"[OK] {sheet_name}: {len(df)} rows")

    connection.close()

    # ========================================================
    # EXPORT TO EXCEL
    # ========================================================

    print("\nCreating Excel workbook...")

    with pd.ExcelWriter(
        OUTPUT_FILE,
        engine="openpyxl"
    ) as writer:

        for sheet_name, df in results.items():

            df.to_excel(
                writer,
                sheet_name=sheet_name,
                index=False
            )

            # Get worksheet
            worksheet = writer.sheets[sheet_name]

            # Freeze header row
            worksheet.freeze_panes = "A2"

            # Auto-adjust column widths
            for column_cells in worksheet.columns:

                max_length = 0
                column_letter = column_cells[0].column_letter

                for cell in column_cells:
                    if cell.value is not None:
                        max_length = max(
                            max_length,
                            len(str(cell.value))
                        )

                worksheet.column_dimensions[
                    column_letter
                ].width = min(max_length + 2, 60)

    # ========================================================
    # COMPLETE
    # ========================================================

    print("\n========================================")
    print("          EXPORT COMPLETE")
    print("========================================")

    print(f"\nExcel file created:")
    print(OUTPUT_FILE)

    print("\nSheets created:")

    for sheet_name in results:
        print(f"- {sheet_name}")

    print("\nYou can now open the Excel file and build")
    print("the dashboard directly from these SQL results.")


if __name__ == "__main__":
    main()