from pathlib import Path
import hashlib
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
            "USER-Agent" : "POLITE-SCRAPER/1.0"
        }
    )

    response.raise_for_status()

    html = response.text
    cache_path.write_text(html, encoding="utf-8")

    time.sleep(REQUEST_DELAY)

    return html

def discover_catalogue(start_url: str) -> list[str]:
    page_url = start_url
    dicovered_url = []
    catalogue_pages = 0
    while page_url and catalogue_pages < MAX_CATALOGUE_PAGES:
        html = fetch_page(page_url)

        catalogue_pages += 1
        soup = BeautifulSoup(html, "html.parser")

        for link in soup.select("article.product_pod h3 a"):
            href = link.get("href")

            if href:
                absolute_url = urljoin(page_url, href)
                dicovered_url.append(absolute_url)

        next_link = soup.select_one("li.next a")

        if next_link:
            page_url = urljoin(page_url, next_link.get("href"))
        else:
            page_url = None

    unique_url = list(dict.fromkeys(dicovered_url))

    print(f"catalogue_pages={catalogue_pages}")
    print(f"discovered={len(dicovered_url)}")
    print(f"unique_urls={len(unique_url)}")

    return unique_url

# def parse_books(html: str) -> list[dict]:
#     soup = BeautifulSoup(html, 'html.parser')

#     books = []

#     for article in soup.select("article.product_pod"):
#         title_element = article.select_one("h3 a")
#         price_element = article.select_one(".price_color")
#         availability_element = article.select_one(".availability")

#         if not title_element:
#                 continue
#         title = title_element.get("title") or title_element.get_text(strip=True)

#         price = (
#              price_element.get_text(strip=True)
#              if price_element
#              else None
#         )
#         availability = (
#              availability_element.get_text("",strip=True)
#              if price_element
#              else None
#         )

#         books.append(
#              {
#                   "Title" : title,
#                   "Price" : price,
#                   "Availability" : availability
#              }
#         )
#     return books
        

   

if __name__ == "__main__":
    start_url = f"{BASE_URL}/"

    discover_catalogue(start_url)

    # books = parse_books(html)

    # print(f"Books found {len(books)}")

    # for book in books:
    #      print(book)

    

