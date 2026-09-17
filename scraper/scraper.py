"""
scraper.py

Scrapes book listings from https://books.toscrape.com/ and saves them
as a raw CSV file for later cleaning and analysis.

For every book we collect:
    - title
    - price          (raw, as shown on the site, e.g. "£51.77")
    - rating         (raw text, e.g. "Three")
    - availability   (raw text, e.g. "In stock (22 available)")
    - category
    - product_url
    - scraped_date   (the date this script was run)

Design:
    get_page()        -> downloads and parses one page of HTML
    parse_book()       -> pulls title/price/rating/availability/url out
                          of one book "tile" on a listing page
    get_book_details() -> visits a single book's own page to read its
                          category (category isn't shown on the
                          listing pages, only on each book's page)
    scrape_books()      -> the main loop: walks every listing page,
                          follows pagination, and calls the two
                          functions above for every book
"""

import time
from datetime import date
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

START_URL = "https://books.toscrape.com/catalogue/page-1.html"

# Books to Scrape is a sandbox built for practicing scraping, but it's
# still good practice to identify ourselves and to be a "polite" client.
HEADERS = {
    "User-Agent": "BookMarketAnalysisBot/1.0 (educational portfolio project)"
}
REQUEST_TIMEOUT = 10  # seconds
REQUEST_DELAY = 0.5   # short pause between requests so we don't hammer the site

# Output path is anchored to this script's location, so the scraper saves
# to the right place whether it's run from the project root or from
# inside the scraper/ folder.
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "books_raw.csv"


def get_page(url):
    """
    Download a page and return a BeautifulSoup object for it.

    Returns None if the request fails, so callers can decide how to
    handle a missing page instead of the whole script crashing.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()  # raises an error for 4xx/5xx responses
    except requests.RequestException as error:
        print(f"  [!] Failed to fetch {url}: {error}")
        return None

    return BeautifulSoup(response.text, "html.parser")


def parse_book(book_tile, page_url):
    """
    Extract the basic fields for one book from its listing-page "tile"
    (an <article class="product_pod"> element).

    Category is NOT included here, since it isn't shown on listing
    pages -- that's fetched separately in get_book_details().

    Returns a dict of fields, or None if the tile is missing data we
    can't safely guess (so one bad book doesn't stop the whole scrape).
    """
    try:
        title_tag = book_tile.h3.a
        title = title_tag["title"].strip()

        # Links on listing pages are relative (e.g. "some-book_123/index.html").
        # requests/bs4 don't resolve relative links automatically, so we
        # build the full URL ourselves using the page we found it on.
        product_url = requests.compat.urljoin(page_url, title_tag["href"])

        price_tag = book_tile.find("p", class_="price_color")
        price = price_tag.get_text(strip=True) if price_tag else None

        availability_tag = book_tile.find("p", class_="instock availability")
        availability = (
            availability_tag.get_text(strip=True) if availability_tag else None
        )

        # Star rating is stored as a CSS class, e.g. class="star-rating Three"
        rating_tag = book_tile.find("p", class_="star-rating")
        rating = None
        if rating_tag:
            classes = rating_tag.get("class", [])
            # The rating word is whichever class isn't "star-rating"
            rating_words = [c for c in classes if c != "star-rating"]
            if rating_words:
                rating = rating_words[0]

    except (AttributeError, KeyError, TypeError) as error:
        print(f"  [!] Skipping a book due to unexpected HTML: {error}")
        return None

    if not title or not product_url:
        # Title and URL are essential; without them the row isn't useful.
        print("  [!] Skipping a book with missing title/url")
        return None

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "availability": availability,
        "product_url": product_url,
    }


def get_book_details(product_url):
    """
    Visit a single book's own page and return its category.

    Category lives in the breadcrumb trail at the top of the page:
        Home > Books > <Category> > <Book Title>
    so the category is always the second-to-last breadcrumb item.

    Returns None if the category can't be found, rather than crashing.
    """
    soup = get_page(product_url)
    if soup is None:
        return None

    try:
        breadcrumb_items = soup.find("ul", class_="breadcrumb").find_all("li")
        # breadcrumb_items looks like: [Home, Books, Category, Book Title]
        category = breadcrumb_items[-2].get_text(strip=True)
    except (AttributeError, IndexError):
        print(f"  [!] Could not find category for {product_url}")
        return None

    return category


def scrape_books():
    """
    Main scraping loop.

    Walks every listing page starting at page 1, following the "next"
    pagination link until there isn't one, and builds up a list of
    book records (as dicts) along the way.
    """
    all_books = []
    page_url = START_URL
    page_number = 1

    while page_url:
        print(f"Scraping page {page_number}: {page_url}")
        soup = get_page(page_url)

        if soup is None:
            # Could not load this page at all -- stop rather than guess
            # what the next page URL might be.
            print("  [!] Stopping: could not load this page.")
            break

        book_tiles = soup.find_all("article", class_="product_pod")
        print(f"  Found {len(book_tiles)} books on this page")

        for tile in book_tiles:
            book = parse_book(tile, page_url)
            if book is None:
                continue  # already logged inside parse_book()

            time.sleep(REQUEST_DELAY)
            book["category"] = get_book_details(book["product_url"])
            book["scraped_date"] = date.today().isoformat()

            all_books.append(book)

        print(f"  Total books collected so far: {len(all_books)}")

        # Look for a "next" link to keep paginating.
        next_link = soup.find("li", class_="next")
        if next_link and next_link.a:
            page_url = requests.compat.urljoin(page_url, next_link.a["href"])
            page_number += 1
            time.sleep(REQUEST_DELAY)
        else:
            page_url = None  # no more pages -- loop will end

    return all_books


def save_to_csv(books, output_path):
    """
    Save the scraped books to a CSV file, removing any accidental
    duplicate rows first (matched on product_url, which is unique
    per book).
    """
    df = pd.DataFrame(books)

    before = len(df)
    df = df.drop_duplicates(subset="product_url", keep="first")
    removed = before - len(df)
    if removed:
        print(f"Removed {removed} duplicate row(s) before saving.")

    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} rows to {output_path}")

    return df


if __name__ == "__main__":
    print("Starting Books to Scrape scraper...\n")

    scraped_books = scrape_books()
    print(f"\nFinished scraping. Total books collected: {len(scraped_books)}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    save_to_csv(scraped_books, OUTPUT_PATH)
