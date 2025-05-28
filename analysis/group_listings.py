import json
import os

def group_listings():
    with open("data/unegui_api_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    groups = {
        "Орон сууц зарна": [], "Түрээсийн байр": [],
        "Газар зарна": [], "Оффис зарна": [],
        "Оффис түрээслүүлнэ": [], "Хашаа байшин, Монгол гэр зарна": []
    }

    for item in data:
        title = item.get("title", "").lower()
        desc = (item.get("description") or "").lower()
        if "зарна" in title or "зарна" in desc:
            if "газар" in title:
                groups["Газар зарна"].append(item)
            elif "хашаа" in title or "гэр" in title:
                groups["Хашаа байшин, Монгол гэр зарна"].append(item)
            elif "оффис" in title:
                groups["Оффис зарна"].append(item)
            else:
                groups["Орон сууц зарна"].append(item)
        elif "түрээслүүлнэ" in title:
            if "оффис" in title:
                groups["Оффис түрээслүүлнэ"].append(item)
            else:
                groups["Түрээсийн байр"].append(item)
        else:
            groups["Түрээсийн байр"].append(item)

    os.makedirs("analysis", exist_ok=True)
    with open("analysis/grouped_listings.json", "w", encoding="utf-8") as f:
        json.dump(groups, f, ensure_ascii=False, indent=4)
    print("6 бүлэг үүсгэж хадгаллаа.")
