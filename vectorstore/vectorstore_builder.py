import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer

# Модел ачаалах
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# JSON өгөгдөл унших
with open("data/unegui_api_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Embedding үүсгэх текстүүд бэлдэх (title + description)
texts = [f"{item['title']} - {item['description']}" for item in data]
embeddings = model.encode(texts)

# FAISS index үүсгэх
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings, dtype=np.float32))

# Index хадгалах
faiss.write_index(index, "vectorstore/real_estate.index")

# Texts хадгалах
with open("vectorstore/texts.json", "w", encoding="utf-8") as f:
    json.dump(texts, f, ensure_ascii=False, indent=4)

# Original data хадгалах
with open("vectorstore/original_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"✅ Vectorstore үүсэж хадгалагдлаа: {len(data)} items.")
