import json, os
from fpdf import FPDF
from chain_of_thought.chain_of_thought_reasoner import generate_reasoning

def generate_pdf(query=""):
    with open("analysis/grouped_listings.json", "r", encoding="utf-8") as f:
        grouped = json.load(f)

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'report/DejaVuSans.ttf', uni=True)
    pdf.set_font("DejaVu", size=14)
    pdf.cell(0, 10, f"Үл хөдлөх хөрөнгийн туслах тайлан: {query}", ln=True)

    for group_name, items in grouped.items():
        pdf.set_font("DejaVu", size=12)
        pdf.cell(0, 10, f"Бүлэг: {group_name} ({len(items)} зар)", ln=True)
        pdf.set_font("DejaVu", size=10)
        for item in items[:5]:
            reasoning = generate_reasoning(query, item) if group_name == "Chain-of-Thought" else ""
            pdf.multi_cell(0, 6, f"{item['title']} - {item['price']}₮\n{item['description'][:100]}...\n{item['link']}\nReasoning: {reasoning}\n")
        pdf.ln(5)

    try:
        with open("chain_of_thought/web_results.json", "r", encoding="utf-8") as f:
            web_results = json.load(f)
        pdf.add_page()
        pdf.set_font("DejaVu", size=12)
        pdf.cell(0, 10, "🌐 Интернетээс олдсон вэб үр дүн (Tavily API):", ln=True)
        pdf.set_font("DejaVu", size=10)
        for result in web_results:
            pdf.multi_cell(0, 6, f"{result['title']}\n{result['snippet']}\n{result['url']}\n")
    except FileNotFoundError:
        pdf.multi_cell(0, 6, "Интернетээс үр дүн олдсонгүй.")

    os.makedirs("report", exist_ok=True)
    pdf.output("report/real_estate_report.pdf")
    print("✅ Тайлан PDF болгон хадгаллаа.")
