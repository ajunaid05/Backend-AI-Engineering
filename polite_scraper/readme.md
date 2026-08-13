# The Polite Scraper

A small, polite web scraper for the [Books to Scrape](https://books.toscrape.com/) practice sandbox.

---

## Target Classification

| Attribute | Detail |
|---|---|
| **Target** | Books to Scrape |
| **Purpose** | Books to Scrape is a practice sandbox intended for learning and testing web scraping. |
| **Scope** | This scraper processes only the first three catalogue pages and collects the books available on those pages. |
| **Robots.txt** | Checked at `https://books.toscrape.com/robots.txt`. The endpoint returned `404 Not Found`, so no robots.txt directives were available at this URL to evaluate. |
| **Lane** | Backend AI Engineering — web scraping / data collection. |

---

## Installation

Create and activate the project's virtual environment, then install the required Python packages:

```bash
pip install requests beautifulsoup4 pydantic
```

---

## Run Command

From the project directory, run:

```bash
python src/main.py
```

---

## What the Scraper Does

The scraper:

1. Discovers books from the first three catalogue pages.
2. Converts relative links into absolute canonical URLs.
3. Fetches each book page.
4. Extracts the book details.
5. Normalizes the price.
6. Validates each record with Pydantic.
7. Writes the valid records to `books.json`.

---

## Record Schema

| Field | Type | Requirement |
|---|---|---|
| `title` | `str` | Required |
| `product_url` | `HttpUrl` | Required; canonical product URL |
| `price_text` | `str` | Required; original scraped price |
| `price_gbp` | `float` | Required; normalized numeric price |
| `availability_text` | `str` | Required |
| `rating_text` | `str` | Required |
| `description` | `str \| None` | Optional |
| `source_page` | `HttpUrl` | Required |
| `fetched_at` | `str` | Required |

---

## Normalization and Validation

- The raw `price_text` value is preserved alongside the cleaned `price_gbp` value. For example, `£51.77` becomes `51.77` as a float.
- Every record is validated using the `BookRecord` Pydantic model before it is stored.
- Records that fail extraction, normalization, or validation are **not** written to `books.json`. They are recorded in `errors.json` with the product URL and the reason for failure.

---

## Identity and Idempotency

- The absolute `product_url` is used as the identity of a book.
- Catalogue URLs are stored in a dictionary, so duplicate URLs are represented only once.
- Re-running the scraper therefore does not append duplicate records; the output is regenerated from the same discovered URLs.

---

## Politeness Rules

- A custom User-Agent is sent: `POLITE-SCRAPER/1.0`.
- Requests use a 10-second timeout.
- A 0.5-second delay is used after requests.
- Downloaded pages are cached locally in `cache/`.
- Cached pages are reused on later runs instead of requesting them again.
- Timeouts and 5xx server errors are retried once.
- 404 responses are not retried.
- 403 responses are not retried.

---

## Failure Handling

Each book page is handled independently. A failed page is caught, logged, and skipped so that one bad page does not terminate the entire scraping run.

In the Stage 5 test, one deliberately fake URL produced a 404 while the other 60 valid records still completed successfully.

---

## Output Files

| File | Description |
|---|---|
| `output/books.json` | Valid, normalized, and validated book records. |
| `output/errors.json` | Failed pages and their reasons. |
| `output/run-report.json` | Summary statistics for the run. |

---

## Run Report Evidence

A real Stage 5 run produced the following report:

```json
{
  "start_time": "2026-08-13T22:32:15.821611+00:00",
  "duration_seconds": 1.721171,
  "pages_fetched": 0,
  "cache_hits": 63,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 1
}
```

The run intentionally included one fake product URL. It failed with HTTP 404, while the 60 valid records survived and were written successfully.

---

## Why No Browser Is Needed

This assignment needs no browser because the data is already in the HTML the server sends, so a browser would only add cost.

---

## Browser and Data-Access Principle

The scraper uses direct HTTP requests because the required book data is present in the server-delivered HTML. Browser automation is therefore unnecessary for this target.

---

## Ethical Use

- Use an official API when one exists.
- Never bypass logins, paywalls, or blocks.
- Collect only what you need.

This project is limited to the designated practice sandbox. This code will not be reused on another site without checking its rules and terms first.

---

## Honest Limitation

The scraper intentionally processes only the first three catalogue pages, so it does not represent the complete Books to Scrape catalogue.

---

## Author

**Ahmad Junaid**

Backend AI Engineering – Assignment 1

COMSATS University Islamabad