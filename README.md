# Үл хөдлөх хөрөнгийн туслах

## 🏠 Дэлгэрэнгүй

Machine Learning final assignment ба үл хөдлөх хөрөнгийн зах зээлийн заруудыг (unegui.mn) цуглуулж, ангилж, дүн шинжилгээ хийж, тайлан гаргах **Python төсөл** болно.  
Төслийн оноо хуваалт:

✅ unegui.mn сайт руу автомат хайлт хийж, мэдээлэл татах  
✅ Зарын мэдээллийг ангилж бүлэглэх  
✅ Chain-of-Thought reasoning (утга, логик дүгнэлт) ашиглах  
✅ Vectorstore (FAISS) хайлтын системээр заруудыг ижил төстэй байдлаар бүлэглэх
✅ Интернэтээс шууд хайлт хийх (Tavily API ашиглан)  
✅ Бүх мэдээллийг PDF тайлангаар үүсгэж хадгалах

---

## 🧩 Ашигласан технологиуд

| Технологи              | Үүрэг                                   |
|------------------------|------------------------------------------|
| Python                 | Гол програмчлалын хэл                     |
| requests               | unegui.mn API болон Tavily API холболт    |
| json                   | Өгөгдөл хадгалах, унших                    |
| PIL (Pillow)           | Зураг боловсруулах, формат хөрвүүлэх       |
| FPDF                   | PDF тайлан үүсгэх                         |
| Sentence-Transformers  | Текст embedding үүсгэх, FAISS-д ашиглах   |
| FAISS                  | Vectorstore хайлтын систем                 |
| Tkinter                | Хэрэглэгчийн жижиг интерфэйс (UI)               |
| Tavily API             | Интернэтээс real-time хайлт хийх           |

---

## 🏗️ Фолдерын бүтэц

real-estate-assistant/
├── analysis/
│ └── group_listings.py
├── chain_of_thought/
│ └── chain_of_thought_reasoner.py
├── data/
│ └── unegui_scraper.py
├── report/
│ └── pdf_report_generator.py
├── search/
│ └── web_search.py
├── vectorstore/
│ ├── vectorstore_builder.py
│ └── vectorstore_search.py
├── report/
│ ├── DejaVuSans.ttf
├── main.py
└── README.md


---

## 🚀 Яаж ажиллуулах вэ?

### 1️⃣ **Орчны бэлтгэл**

✅ Шаардлагатай сангуудыг суулгах:
```bash
pip install requests faiss-cpu sentence-transformers numpy fpdf2 tk

✅ .env файл үүсгэж, өөрийн Tavily API түлхүүрээ оруулах:
TAVILY_API_KEY=YOUR_API_KEY_HERE

2️⃣ Системийг ажиллуулах
Төслийн үндсэн фолдер дээр:

python main.py


3️⃣ Tkinter UI дээр дараах алхамууд хийгдэнэ:
Хайлтын түлхүүр үг оруулах(Энэ нь интернэтээс real-time хайлт хийх утга болно)

"Тайлан үүсгэх" товч дарах

Систем явцын дарааллаар:

    -unegui.mn-ээс өгөгдөл татна

    -FAISS vectorstore үүсгэнэ

    -Зар ангилж бүлэглэнэ

    -Интернэтээс хайлт хийнэ (Tavily API)

    -Reasoning болон зурагтай PDF тайлан үүсгэнэ

    -Бүх мэдээллийг report/real_estate_report.pdf файлд хадгална

📄 Тайлангийн бүтэц
Тайланд дараах мэдээлэл орно:

Бүлэглэсэн зарын мэдээлэл (Орон сууц зарна, Түрээсийн байр гэх мэт)

Зарын гарчиг, үнэ, тайлбар, зураг, reasoning дүгнэлт

Vectorstore recommendation (ижил төстэй зарууд)

Интернетээс хайсан үр дүн

Chain-of-Thought reasoning (чухал дүгнэлтүүд)

📌 Жишээ ашиглалт

Хайлтын түлхүүр үг: 3 өрөө байр
→ Тайлан гарна: report/real_estate_report.pdf


🛡️ Анхаарах зүйлс
FAISS хайлтын хэсэг зөв ажиллахын тулд data/unegui_api_data.json файл байх ёстой (unegui_scraper ашиглан автоматаар татна)

Tavily API-г ашиглахын тулд TAVILY_API_KEY заавал оруулсан байх шаардлагатай

PDF файл том (олон зарын үед 10+ MB) болж болзошгүй тул хэрэглэхдээ анхаараарай