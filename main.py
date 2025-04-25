from fastapi import FastAPI, HTTPException
import requests
import os

app = FastAPI()

# Получаем API ключ из переменных окружения
API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")

if not API_KEY:
    raise RuntimeError("GOOGLE_PLACES_API_KEY is not set. Please add it as an environment variable.")

@app.get("/find_company")
def find_company(query: str, city: str):
    full_query = f"{query} {city}"
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": full_query,
        "key": API_KEY,
        "language": "de"
    }
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="Google Places API error")
    data = resp.json()
    results = []
    for place in data.get("results", []):
        results.append({
            "name": place.get("name"),
            "address": place.get("formatted_address"),
            "place_id": place.get("place_id")
        })
    return {"companies": results}
