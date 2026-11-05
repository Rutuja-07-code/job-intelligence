
import os

import requests
from dotenv import load_dotenv

load_dotenv()


def test_adzuna_connection():
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")

    if not app_id or not app_key:
        raise ValueError("Adzuna credentials are missing from .env")

    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"

    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": 1,
        "what": "python developer",
        "where": "India",
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    data = response.json()
    if data.get("results"):
        print(data["results"][0])
    else:
        print("No jobs returned")

    return {
        "total_results": data.get("count", 0),
        "jobs_returned": len(data.get("results", [])),
        "first_job_title": (
            data["results"][0].get("title")
            if data.get("results")
            else None
        ),
    }
def fetch_jobs(
    keyword: str,
    location: str,
    results_per_page: int = 10
):
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")

    if not app_id or not app_key:
        raise ValueError("Adzuna credentials are missing from .env")

    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"

    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": results_per_page,
        "what": keyword,
        "where": location,
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    data = response.json()

    return data.get("results", [])