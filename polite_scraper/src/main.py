import requests

BASE_URL = "https://books.toscrape.com"


def fetch_page(url: str) -> str:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


if __name__ == "__main__":
    url = f"{BASE_URL}/"
    html = fetch_page(url)

    print(f"Fetched {len(html)} characters from {url}")