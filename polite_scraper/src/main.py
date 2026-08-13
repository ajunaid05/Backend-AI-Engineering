from pathlib import Path
import hashlib
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import time


BASE_URL = "https://books.toscrape.com"
CACHE_DIR = Path("cache")
MAX_CATALOGUE_PAGES = 3
REQUEST_DELAY = 0.5


def get_cache_path(url: str) -> Path:
    file_name = hashlib.sha256(url.encode()).hexdigest() + ".html"
    return CACHE_DIR / file_name


def fetch_page(url: str) -> str:
    CACHE_DIR.mkdir(exist_ok=True)

    cache_path = get_cache_path(url)

    if cache_path.exists():
        print(f"Cache Hit: {url}")
        return cache_path.read_text(encoding="utf-8")

    print(f"Fetching: {url}")

    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "POLITE-SCRAPER/1.0"
        }
    )

    response.raise_for_status()
    response.encoding = response.apparent_encoding


    html = response.text
    cache_path.write_text(html, encoding="utf-8")

    time.sleep(REQUEST_DELAY)

    return html


def discover_catalogue(start_url: str) -> dict[str, str]:
    page_url = start_url
    discovered_urls = {}
    catalogue_pages = 0

    while page_url and catalogue_pages < MAX_CATALOGUE_PAGES:
        html = fetch_page(page_url)

        catalogue_pages += 1
        soup = BeautifulSoup(html, "html.parser")

        for link in soup.select("article.product_pod h3 a"):
            href = link.get("href")

            if href:
                absolute_url = urljoin(page_url, href)
                discovered_urls[absolute_url] = page_url

        next_link = soup.select_one("li.next a")

        if next_link:
            page_url = urljoin(page_url, next_link.get("href"))
        else:
            page_url = None

    unique_urls = list(discovered_urls.keys())

    print(f"catalogue_pages={catalogue_pages}")
    print(f"discovered={len(discovered_urls)}")
    print(f"unique_urls={len(unique_urls)}")

    return discovered_urls


def extract_book_details(
    html: str,
    product_url: str,
    source_page: str,
    fetched_at: str
) -> dict:

    soup = BeautifulSoup(html, "html.parser")

    product = soup.select_one("article.product_page")

    if not product:
        raise ValueError(f"Product area not found: {product_url}")

    title_element = product.select_one("h1")
    price_element = product.select_one(".price_color")
    availability_element = product.select_one(".availability")
    rating_element = product.select_one("p.star-rating")
    description_element = product.select_one("#product_description + p")

    title = (
        title_element.get_text(strip=True)
        if title_element
        else None
    )

    price_text = (
        price_element.get_text(strip=True)
        if price_element
        else None
    )

    availability_text = (
        availability_element.get_text(" ", strip=True)
        if availability_element
        else None
    )

    rating_text = (
        " ".join(rating_element.get("class", [])[1:])
        if rating_element
        else None
    )

    description = (
        description_element.get_text(" ",strip=True)
        if description_element
        else None
    )

    return {
        "title": title,
        "product_url": product_url,
        "price_text": price_text,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": fetched_at
    }


def extract_all_books(book_sources: dict[str, str]) -> list[dict]:
    records = []

    for product_url, source_page in book_sources.items():
        html = fetch_page(product_url)

        fetched_at = datetime.now(timezone.utc).isoformat()

        record = extract_book_details(
            html=html,
            product_url=product_url,
            source_page=source_page,
            fetched_at=fetched_at
        )

        records.append(record)

    return records


if __name__ == "__main__":
    start_url = f"{BASE_URL}/"

    book_sources = discover_catalogue(start_url)

    records = extract_all_books(book_sources)

    print(f"detail_pages={len(records)}")

    if records:
        print(records[0])