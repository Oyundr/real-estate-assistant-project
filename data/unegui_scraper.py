import requests
import json
import time
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "mn,en;q=0.9"
}

RUBRICS = [3721, 3723]  # Байр, Үйлчилгээний талбай
BASE_URL = "https://www.unegui.mn/api/items/?rubric={}&page={}"

def scrape_unegui():
    all_listings = []
    for rubric in RUBRICS:
        print(f"\n--- Scraping rubric: {rubric} ---")
        page = 1
        while True:
            url = BASE_URL.format(rubric, page)
            try:
                response = requests.get(url, headers=HEADERS, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    if not results:
                        print(f"No more data at page {page}. Finished scraping rubric {rubric}.")
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
                    print(f"Rubric {rubric}, Page {page} scraped: {len(results)} items.")
                elif response.status_code == 403:
                    print(f"403 Forbidden at {url}. Sleeping 10s and retrying...")
                    time.sleep(10)
                elif response.status_code == 404:
                    print(f"404 Not Found at {url}. Skipping to next rubric...")
                    break
                else:
                    print(f"Error {response.status_code} at {url}. Skipping...")
            except requests.exceptions.RequestException as e:
                print(f"Request error at {url}: {e}")
            page += 1
            time.sleep(2)  # Хэт хурдан хандахаас сэргийлэх

    os.makedirs("data", exist_ok=True)
    with open("data/unegui_api_data.json", "w", encoding="utf-8") as f:
        json.dump(all_listings, f, ensure_ascii=False, indent=4)
    print(f"\n Бүх rubric-уудаас нийт {len(all_listings)} listings хадгаллаа.")

if __name__ == "__main__":
    scrape_unegui()
