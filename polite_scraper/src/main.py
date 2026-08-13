from pathlib import Path
import hashlib
import requests

BASE_URL = "https://books.toscrape.com"
CACHE_DIR = Path("cache")

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

    return html

if __name__ == "__main__":
    url = f"{BASE_URL}/"
    html = fetch_page(url)

    print(f"Fetched {len(html)} characters.") 