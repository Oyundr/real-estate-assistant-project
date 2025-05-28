def generate_reasoning(query, item):
    reasoning = []

    # Хайлтын хамаарал дүгнэлт
    title = item.get('title', '').lower()
    description = item.get('description', '').lower()
    query_lower = query.lower()

    if query_lower in title and query_lower in description:
        reasoning.append("🔍 Хайлтын түлхүүр үг гарчиг болон тайлбарт хоёуланд орсон - Өндөр хамааралтай зар")
    elif query_lower in title:
        reasoning.append("🔍 Хайлтын түлхүүр үг зөвхөн гарчигт орсон - Голлох сэдэвтэй зар")
    elif query_lower in description:
        reasoning.append("🔍 Хайлтын түлхүүр үг зөвхөн тайлбарт орсон - Сул хамааралтай зар")
    else:
        reasoning.append("🔍 Хайлтын түлхүүр үг олдсонгүй - Та хайлтаа дахин шалгаарай")

    # Байршлын дүгнэлт
    location = item.get('location', 'Байршил тодорхойгүй')
    reasoning.append(f"📍 Байршил: {location}")

    # Үнэ, валютын дүгнэлт
    price = item.get('price', None)
    currency = item.get('currency', '')
    if price is not None:
        price_val = int(price)
        if price_val > 1000000000:
            reasoning.append(f"Маш өндөр үнэ ({price}{currency}) - Luxury ангилал")
        elif price_val > 500000000:
            reasoning.append(f"Өндөр үнэ ({price}{currency}) - Дундаж ангилал")
        elif price_val < 100000000:
            reasoning.append(f"Хямд үнэ ({price}{currency}) - Affordable ангилал")
        else:
            reasoning.append(f"Дундаж үнэ ({price}{currency})")
    else:
        reasoning.append("Үнэ тодорхойгүй - Холбогдож лавлах шаардлагатай")

    # Зургийн дүгнэлт
    images = item.get('images', [])
    if isinstance(images, list) and len(images) > 0:
        reasoning.append(f"{len(images)} зурагтай - Visual content сайн")
    else:
        reasoning.append("Зураг байхгүй - Visual data дутуу")

    # Зар оруулагчийн мэдээлэл
    user = item.get('user')
    if user:
        reasoning.append(f"👤 Зар оруулагч: {user}")
    else:
        reasoning.append("👤 Эзэмшигчийн мэдээлэл байхгүй")

    # Эцсийн дүгнэлт
    summary = []
    if price and int(price) > 1000000000:
        summary.append("Энэ үл хөдлөх маш өндөр үнэтэй бөгөөд хөрөнгө оруулалтын ангилалд тохиромжтой.")
    if len(images) >= 5:
        summary.append("Олон зурагтай тул хэрэглэгчийн сонирхлыг их татах боломжтой.")
    if "түлхүүр үг олдсонгүй" in reasoning[0]:
        summary.append("Хайлтын түлхүүр үг тохирохгүй тул дахин шалгах шаардлагатай.")

    if summary:
        reasoning.append("Дүгнэлт: " + " ".join(summary))

    return " | ".join(reasoning)
