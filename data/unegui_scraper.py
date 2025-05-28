import requests
import json
import time

BASE_URL = "https://www.unegui.mn/api/items/?rubric=1720&page={}"

all_listings = []

for page in range(1, 4):  # Эхний 3 хуудсыг авна
    url = BASE_URL.format(page)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        for item in results:
            coordinates = item.get("coordinates") or {}  # Хэрвээ None бол хоосон dict
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

        print(f"Page {page} scraped. {len(results)} items.")
    else:
        print(f"Error fetching page {page}")
    
    time.sleep(1)

# JSON файлд хадгалах
with open("data/unegui_api_data.json", "w", encoding="utf-8") as f:
    json.dump(all_listings, f, ensure_ascii=False, indent=4)

print(f"🎉 {len(all_listings)} listings saved to data/unegui_api_data.json")
