import json

def group_listings():
    with open("vectorstore/original_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    groups = {
        "Орон сууц зарна": [],
        "Түрээсийн байр": [],
        "Газар зарна": [],
        "Оффис болон үйлчилгээний талбай": [],
        "Chain-of-Thought": []
    }

    for item in data:
        title = item["title"].lower()
        desc = (item["description"] or "").lower()

        if "зарна" in title or "зарна" in desc:
            if "газар" in title or "газар" in desc:
                groups["Газар зарна"].append(item)
            elif "байр" in title or "өрөө" in title or "байр" in desc:
                groups["Орон сууц зарна"].append(item)
            else:
                groups["Chain-of-Thought"].append(item)
        elif "түрээслүүлнэ" in title or "түрээс" in title or "түрээслэнэ" in desc:
            groups["Түрээсийн байр"].append(item)
        elif "офис" in title or "үйлчилгээний" in title or "талбай" in title:
            groups["Оффис болон үйлчилгээний талбай"].append(item)
        else:
            groups["Chain-of-Thought"].append(item)

    with open("analysis/grouped_listings.json", "w", encoding="utf-8") as f:
        json.dump(groups, f, ensure_ascii=False, indent=4)

    print("✅ 5 бүлгийн мэдээлэл үүсгэлээ.")
