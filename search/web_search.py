import requests
import json
import os

API_KEY = os.getenv("TAVILY_API_KEY")
if not API_KEY:
    raise ValueError("TAVILY_API_KEY орчны хувьсагч тохируулаагүй байна!")

def search_web_results(query):
    endpoint = "https://api.tavily.com/search"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"query": query, "search_depth": "basic", "max_results": 5}
    
    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        if response.status_code == 200:
            results = response.json().get("results", [])
            web_data = [{"title": r["title"], "snippet": r["content"], "url": r["url"]} for r in results]
            os.makedirs("chain_of_thought", exist_ok=True)
            with open("chain_of_thought/web_results.json", "w", encoding="utf-8") as f:
                json.dump(web_data, f, ensure_ascii=False, indent=4)
            print("Интернетээс үр дүн хадгаллаа.")
            return web_data
        else:
            print(f"Алдаа: {response.status_code}")
            return []
    except Exception as e:
        print(f"Web хайлтад алдаа: {e}")
        return []
