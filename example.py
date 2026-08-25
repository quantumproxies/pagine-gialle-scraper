"""Minimal Business directory API call — one typed row per business.

Docs & schema: https://quanticdata.io/collectors/business-directory-api/
"""
import json
import os

import requests

API = "https://api.quanticdata.io/v1/scraper/collectors/business_directory/run"
KEY = os.environ["QD_API_KEY"]  # https://quanticdata.io/

payload = {
        "query": "autonoleggio",
        "location": "Milano",
        "max_results": 25
    }

r = requests.post(
    API,
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    json=payload,
    timeout=180,
)
r.raise_for_status()
data = r.json()["payload"]

for row in data["results"]:
    print(row.get("name"), row.get("category"), row.get("address"))
print(f"{len(data['results'])} businesss, cost ${data['cost']}")
