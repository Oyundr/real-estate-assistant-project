import faiss
import numpy as np
import json
import os
from sentence_transformers import SentenceTransformer

def build_vectorstore(target_group="Түрээсийн байр"):
    model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    with open("analysis/grouped_listings.json", "r", encoding="utf-8") as f:
        grouped = json.load(f)

    if target_group not in grouped:
        print(f"'{target_group}' бүлэг олдсонгүй!")
        return

    data = grouped[target_group]
    if not data:
        print(f"'{target_group}' бүлэгт зар байхгүй!")
        return

    texts = [f"{item.get('title', '')} - {item.get('description', '')}" for item in data]
    embeddings = model.encode(texts)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings, dtype=np.float32))

    os.makedirs("vectorstore", exist_ok=True)
    faiss.write_index(index, "vectorstore/real_estate.index")
    with open("vectorstore/texts.json", "w", encoding="utf-8") as f:
        json.dump(texts, f, ensure_ascii=False, indent=4)

    print(f"Vectorstore үүсгэж хадгаллаа: {len(data)} items from '{target_group}' бүлэг.")
