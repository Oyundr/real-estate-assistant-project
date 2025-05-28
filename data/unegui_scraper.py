import requests
import json
import time
import os

# Custom headers to avoid 403/404 errors
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "mn,en;q=0.9"
}

RUBRICS = [1786, 1814, 1788, 1789, 1730, 1729]
BASE_URL = "https://www.unegui.mn/api/items/?rubric={}&page={}"

def scrape_unegui(pages=3):
    all_listings = []
    for rubric in RUBRICS:
        print(f"\n--- Scraping rubric: {rubric} ---")
        for page in range(1, pages + 1):
            url = BASE_URL.format(rubric, page)
            try:
                response = requests.get(url, headers=HEADERS, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    if not results:
                        print(f" No more data at page {page}. Stopping...")
                        break
                    for item in results:
                        coordinates = item.get("coordinates") or {}
                        listing = {
                            "title": item.get("title"),
                            "description": item.get("description"),
                            "price": item.get("price"),
                            "currency": item.get("currency"),
                            "location": item.get("city"),
                            "districts": item.get("city_districts"),
                            "created_dt": item.get("created_dt"),
                            "user": item.get("user", {}).get("name"),
                            "images": [img.get("url") for img in item.get("images", [])],
                            "latitude": coordinates.get("latitude"),
                            "longitude": coordinates.get("longitude"),
                            "link": f"https://www.unegui.mn/{item.get('slug')}/"
                        }
                        all_listings.append(listing)
                    print(f" Rubric {rubric}, Page {page} scraped: {len(results)} items.")
                elif response.status_code == 403:
                    print(f" 403 Forbidden at {url}. Sleeping 10s and retrying...")
                    time.sleep(10)
                elif response.status_code == 404:
                    print(f" 404 Not Found at {url}. Skipping...")
                    break  # Probably no more pages for this rubric
                else:
                    print(f" Error {response.status_code} at {url}. Skipping...")
            except requests.exceptions.RequestException as e:
                print(f" Request error at {url}: {e}")
            time.sleep(1)  # To avoid too many requests too fast

    os.makedirs("data", exist_ok=True)
    with open("data/unegui_api_data.json", "w", encoding="utf-8") as f:
        json.dump(all_listings, f, ensure_ascii=False, indent=4)
    print(f"\nБүх rubric-уудаас нийт {len(all_listings)} listings хадгаллаа.")

if __name__ == "__main__":
    scrape_unegui(pages=20)
