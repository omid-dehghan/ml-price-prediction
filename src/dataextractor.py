import requests
import csv
import time
from urllib.parse import urlparse

def scrape_tgju_history(history_url, output_file="tgju_history.csv", max_pages=1000, rows_per_page=30, delay=0.5):
    """
    Scrapes TGJU history tables for any symbol (ons, price_dollar_rl, geram18, etc.)
    Just provide the history URL, e.g.:
        scrape_tgju_history("https://www.tgju.org/profile/ons/history")
    """
    # Extract symbol from URL (e.g., "ons", "geram18", "price_dollar_rl")
    path_parts = urlparse(history_url).path.split("/")
    if len(path_parts) < 3:
        raise ValueError("Invalid TGJU history URL")
    symbol = path_parts[2]  # e.g., "ons", "geram18"

    # Base API endpoint for TGJU history tables
    endpoint_base = (
        f"https://api.tgju.org/v1/market/indicator/summary-table-data/{symbol}"
        "?lang=fa&order_dir=asc&convert_to_ad=1"
    )

    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Col1", "Col2", "Col3", "Col4", "Col5", "Col6", "Col7", "Col8"])  # generic headers

        for page in range(max_pages):
            start = page * rows_per_page
            url = f"{endpoint_base}&start={start}&length={rows_per_page}"
            print(f"Fetching page {page+1}: start={start}")

            try:
                resp = requests.get(url, timeout=10)
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                print(f"❌ Error fetching page {page+1}: {e}")
                break

            rows = data.get("data", [])
            if not rows:
                print("✅ No more data, stopping.")
                break

            for row in rows:
                writer.writerow(row)

            time.sleep(delay)

    print(f"\n🎉 Done! Data saved to {output_file}")
