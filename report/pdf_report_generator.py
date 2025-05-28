import os
import json
import requests
from io import BytesIO
from PIL import Image
import re
from fpdf import FPDF
from chain_of_thought.chain_of_thought_reasoner import generate_reasoning
from vectorstore.vectorstore_search import search_vectorstore

def clean_text(text):
    return re.sub(r'[^\x00-\x7F\u0400-\u04FF\u0600-\u06FF\u0900-\u097F\u1100-\u11FF\u3040-\u30FF\u4E00-\u9FFF\s.,;?!:/\'"-]', '', text)

def download_image(url, temp_dir="temp_images"):
    try:
        os.makedirs(temp_dir, exist_ok=True)
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content)).convert("RGB")
            img.thumbnail((100, 100))
            filename = os.path.basename(url).split("?")[0].split(".")[0] + ".jpg"
            temp_path = os.path.join(temp_dir, filename)
            img.save(temp_path, format="JPEG")
            return temp_path
    except Exception as e:
        print(f"Зураг татахад алдаа: {e}")
    return None

def generate_pdf(query=""):
    with open("analysis/grouped_listings.json", "r", encoding="utf-8") as f:
        grouped = json.load(f)

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'report/DejaVuSans.ttf', uni=True)
    pdf.set_font("DejaVu", size=14)
    pdf.cell(0, 10, clean_text("Үл хөдлөх хөрөнгийн туслах тайлан"), ln=True, align="C")
    pdf.set_font("DejaVu", size=11)
    pdf.cell(0, 10, clean_text(f"Хайлтын түлхүүр үг: {query}"), ln=True, align="C")
    pdf.ln(5)

    TARGET_COT_GROUP = "Орон сууц зарна"
    TARGET_VECTOR_GROUP = "Түрээсийн байр"

    group_num = 1
    for group_name, items in grouped.items():
        pdf.set_font("DejaVu", size=12)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 10, clean_text(f"{group_num}. Бүлэг: {group_name} ({len(items)} зар)"), ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("DejaVu", size=10)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)

        if not items:
            pdf.multi_cell(160, 6, clean_text(f"{group_name} бүлэгт мэдээлэл олдсонгүй.\n"))
            continue

        for i, item in enumerate(items, start=1):
            title = clean_text(item.get('title', 'Гарчиг байхгүй'))[:100]
            price = clean_text(str(item.get('price', 'Үнэ тодорхойгүй')))
            description = clean_text(item.get('description', 'Тайлбар байхгүй'))[:150]
            link = item.get('link', '#')

            reasoning_text = ""
            if group_name == TARGET_COT_GROUP:
                reasoning_text = clean_text(f"Reasoning: {generate_reasoning(query, item)}")[:300]
            elif group_name == TARGET_VECTOR_GROUP:
                vector_results = search_vectorstore(query)
                if vector_results:
                    result_text = "\n".join([f"- {clean_text(r)[:80]}" for r in vector_results])
                    reasoning_text = f"Vectorstore Recommendation:\n{result_text}"
                else:
                    reasoning_text = "Vectorstore Recommendation: Үр дүн олдсонгүй."

            # Зураг оруулах
            images = item.get("images", [])
            img_path = None
            if images and isinstance(images, list) and len(images) > 0:
                img_path = download_image(images[0])

            # Text блок
            y_start = pdf.get_y()
            pdf.set_font("DejaVu", size=10)
            pdf.multi_cell(160, 6, f"{group_num}.{i} - {title} - {price}₮\n{description}\n{link}\n{reasoning_text}")
            y_end = pdf.get_y()

            # Зураг блок (текстийн хажуу талд)
            if img_path:
                try:
                    pdf.set_y(y_start)
                    pdf.set_x(170)
                    pdf.image(img_path, w=30)
                    pdf.set_y(y_end)
                    pdf.ln(5)
                except Exception as e:
                    print(f"⚠️ Зураг оруулахад алдаа: {e}")

            pdf.ln(5)

        pdf.ln(5)
        group_num += 1

    try:
        with open("chain_of_thought/web_results.json", "r", encoding="utf-8") as f:
            web_results = json.load(f)
        pdf.add_page()
        pdf.set_font("DejaVu", size=12)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 10, clean_text(f"Интернетээс олдсон үр дүн (хайлтын үг: {query}):"), ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("DejaVu", size=10)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)

        if not web_results:
            pdf.multi_cell(160, 6, clean_text("Интернетээс үр дүн олдсонгүй.\n"))
        else:
            for i, result in enumerate(web_results, start=1):
                title = clean_text(result.get("title", "Гарчиг байхгүй"))[:100]
                snippet = clean_text(result.get("snippet", "Тайлбар байхгүй"))[:150]
                url = result.get("url", "#")
                pdf.multi_cell(160, 6, f"{i}. {title}\n{snippet}\n{url}\n")
                pdf.ln(2)
    except FileNotFoundError:
        pdf.multi_cell(160, 6, clean_text("Интернетээс үр дүн олдсонгүй."))

    os.makedirs("report", exist_ok=True)
    pdf.output("report/real_estate_report.pdf")
    print("✅ Тайлан PDF болгон хадгаллаа.")

    if os.path.exists("temp_images"):
        for file in os.listdir("temp_images"):
            os.remove(os.path.join("temp_images", file))
        os.rmdir("temp_images")
