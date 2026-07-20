import os
from dotenv import load_dotenv
from apify_client import ApifyClient

# 🔥 We REMOVE linkedin_jobs_scraper because your version does not support Query
# Instead: We use a reliable, free HTML scraper for LinkedIn 👇
import requests
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")

if APIFY_API_TOKEN:
    apify_client = ApifyClient(APIFY_API_TOKEN)
else:
    raise ValueError("APIFY_API_TOKEN missing in .env file")


# ---------------------------------------------------------
# FETCH LINKEDIN JOBS — FREE (NO APIFY, NO SCRAPER LIBRARY)
# ---------------------------------------------------------
def fetch_linkedin_jobs(search_query, location="India", rows=60):
    """
    Scrape LinkedIn job cards directly using HTML — 100% free.
    """

    search_query = search_query.replace(" ", "%20")
    location = location.replace(" ", "%20")

    url = f"https://www.linkedin.com/jobs/search/?keywords={search_query}&location={location}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    for job in soup.select(".base-card"):
        title = job.select_one(".base-search-card__title")
        company = job.select_one(".base-search-card__subtitle")
        link = job.select_one("a.base-card__full-link")

        jobs.append({
            "title": title.get_text(strip=True) if title else "N/A",
            "company": company.get_text(strip=True) if company else "N/A",
            "location": location,
            "description": "N/A",
            "date": "N/A",
            "link": link["href"] if link else "",
        })

        if len(jobs) >= rows:
            break

    return jobs


# ---------------------------------------------------------
# FETCH NAUKRI JOBS — USING APIFY
# ---------------------------------------------------------
def fetch_naukri_jobs(search_query, location="india", rows=60):

    run_input = {
        "keyword": search_query,
        "maxJobs": rows,
        "freshness": "all",
        "sortBy": "relevance",
        "experience": "all"
    }

    run = apify_client.actor("alpcnRV9YI9lYVPWk").call(run_input=run_input)

    dataset_id = run.get("defaultDatasetId")
    if not dataset_id:
        return []

    jobs = list(apify_client.dataset(dataset_id).iterate_items())

    return jobs


