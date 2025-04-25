from fastapi import FastAPI
import requests

app = FastAPI()

API_KEY = "AIzaSyBnAHurADs_0Uk0p-8PRJQnEW6lzbIdTCg"

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
    data = resp.json()
    results = []
    for place in data.get("results", []):
        results.append({
            "name": place.get("name"),
            "address": place.get("formatted_address"),
            "place_id": place.get("place_id")
        })
    return {"companies": results}
