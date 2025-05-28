import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer

def search_vectorstore(query, top_k=3):
    model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
    index = faiss.read_index("vectorstore/real_estate.index")

    with open("vectorstore/texts.json", "r", encoding="utf-8") as f:
        texts = json.load(f)

    if not texts:
        print("Vectorstore хоосон байна!")
        return []

    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding, dtype=np.float32), top_k)

    results = []
    for i in I[0]:
        if i == -1:
            continue
        if 0 <= i < len(texts):
            results.append(texts[i])
        else:
            print(f"Index {i} texts.json-ийн хүрээнээс гадуур байна.")
    return results
