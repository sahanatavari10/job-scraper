import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://remoteok.com/remote-python-jobs"
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, "html.parser")

jobs = soup.find_all("tr", class_="job")

job_list = []

for job in jobs:
    title = job.find("h2", itemprop="title").text.strip() if job.find("h2", itemprop="title") else None
    company = job.find("h3", itemprop="name").text.strip() if job.find("h3", itemprop="name") else None
    location = job.find("div", class_="location").text.strip() if job.find("div", class_="location") else "Remote"
    date = job.find("time")
    date_posted = date["datetime"] if date else None

    job_list.append({
        "title": title,
        "company": company,
        "location": location,
        "date_posted": date_posted
    })

df = pd.DataFrame(job_list)

df.to_csv("python_jobs.csv", index=False)

print("Scraping complete. Saved to python_jobs.csv.")