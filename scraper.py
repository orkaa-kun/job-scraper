import json
import os
from collections import Counter
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup


def scrape_jobs(keyword):
    """
    Scrape jobs from the website and filter them using the given keyword.
    """

    url = "https://realpython.github.io/fake-jobs/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

    except requests.exceptions.RequestException as error:
        print(f"\nError accessing website:\n{error}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    job_cards = soup.find_all("div", class_="card-content")

    jobs = []

    for job in job_cards:

        title_tag = job.find("h2")
        company_tag = job.find("h3")
        location_tag = job.find("p", class_="location")
        link_tag = job.find("a")

        title = title_tag.get_text(strip=True) if title_tag else "N/A"
        company = company_tag.get_text(strip=True) if company_tag else "N/A"
        location = location_tag.get_text(strip=True) if location_tag else "N/A"

        apply_link = (
            link_tag.get("href", "N/A")
            if link_tag
            else "N/A"
        )

        searchable_text = f"{title} {company} {location}"

        if keyword.lower() not in searchable_text.lower():
            continue

        jobs.append(
            {
                "title": title,
                "company": company,
                "location": location,
                "apply_link": apply_link,
            }
        )

    jobs.sort(key=lambda job: (job["company"], job["title"]))

    return jobs


def save_jobs(jobs, keyword):
    """
    Save job data to CSV, Excel and JSON.
    """

    os.makedirs("output", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    csv_file = os.path.join(
        "output",
        f"{keyword}_{timestamp}.csv",
    )

    excel_file = os.path.join(
        "output",
        f"{keyword}_{timestamp}.xlsx",
    )

    json_file = os.path.join(
        "output",
        f"{keyword}_{timestamp}.json",
    )

    dataframe = pd.DataFrame(jobs)

    dataframe.to_csv(csv_file, index=False)

    dataframe.to_excel(excel_file, index=False)

    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(
            jobs,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print("\nFiles created successfully")
    print("-" * 45)
    print(csv_file)
    print(excel_file)
    print(json_file)


def show_summary(jobs, keyword):
    """
    Display scraping statistics.
    """

    print("\n" + "=" * 50)
    print("SCRAPING SUMMARY")
    print("=" * 50)

    print(f"Keyword searched : {keyword}")
    print(f"Jobs found       : {len(jobs)}")

    companies = [job["company"] for job in jobs]

    print(f"Unique companies : {len(set(companies))}")

    if companies:

        print("\nTop Companies")
        print("-" * 45)

        counts = Counter(companies)

        for company, total in counts.most_common(5):
            print(f"{company:<35} {total}")

    print("\nFirst Five Results")
    print("-" * 45)

    for index, job in enumerate(jobs[:5], start=1):

        print(f"\nJob #{index}")
        print(f"Title      : {job['title']}")
        print(f"Company    : {job['company']}")
        print(f"Location   : {job['location']}")
        print(f"Apply Link : {job['apply_link']}")


def main():

    print("=" * 50)
    print("PYTHON JOB SCRAPER")
    print("=" * 50)

    keyword = input("Enter keyword: ").strip()

    if not keyword:
        print("Keyword cannot be empty.")
        return

    jobs = scrape_jobs(keyword)

    if not jobs:
        print(f"\nNo jobs found matching '{keyword}'")
        return

    save_jobs(jobs, keyword)

    show_summary(jobs, keyword)


if __name__ == "__main__":
    main()