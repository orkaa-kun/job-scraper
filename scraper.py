import requests
import pandas as pd
import json
import os

from bs4 import BeautifulSoup
from datetime import datetime
from collections import Counter


def scrape_jobs(keyword):
    """
    Scrape jobs from the website and filter by keyword.
    """

    url = "https://realpython.github.io/fake-jobs/"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"\nError accessing website: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    job_cards = soup.find_all("div", class_="card-content")

    jobs = []

    for job in job_cards:

        title_tag = job.find("h2")
        company_tag = job.find("h3")
        location_tag = job.find("p", class_="location")
        link_tag = job.find("a")

        title = title_tag.text.strip() if title_tag else "N/A"
        company = company_tag.text.strip() if company_tag else "N/A"
        location = location_tag.text.strip() if location_tag else "N/A"

        search_text = f"{title} {company} {location}"

        if keyword.lower() not in search_text.lower():
            continue

        apply_link = (
            link_tag.get("href", "N/A")
            if link_tag else "N/A"
        )

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "apply_link": apply_link
        })

    jobs.sort(key=lambda job: job["company"])

    return jobs


def save_jobs(jobs, keyword):
    """
    Save jobs to CSV, Excel, and JSON files.
    """

    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    csv_file = os.path.join(
        output_folder,
        f"{keyword}_{timestamp}.csv"
    )

    excel_file = os.path.join(
        output_folder,
        f"{keyword}_{timestamp}.xlsx"
    )

    json_file = os.path.join(
        output_folder,
        f"{keyword}_{timestamp}.json"
    )

    df = pd.DataFrame(jobs)

    df.to_csv(csv_file, index=False)
    df.to_excel(excel_file, index=False)

    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(
            jobs,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nFILES CREATED")
    print("-" * 40)
    print(csv_file)
    print(excel_file)
    print(json_file)

    return csv_file, excel_file, json_file


def show_summary(jobs, keyword):
    """
    Display summary statistics.
    """

    print("\nSCRAPING SUMMARY")
    print("-" * 40)

    print(f"Keyword searched : {keyword}")
    print(f"Jobs found       : {len(jobs)}")

    companies = [job["company"] for job in jobs]

    print(f"Unique companies : {len(set(companies))}")

    if companies:

        company_counts = Counter(companies)

        print("\nTop Companies")
        print("-" * 40)

        for company, count in company_counts.most_common(5):
            print(f"{company}: {count}")

    if jobs:

        print("\nSample Results")
        print("-" * 40)

        for job in jobs[:5]:

            print(f"Title    : {job['title']}")
            print(f"Company  : {job['company']}")
            print(f"Location : {job['location']}")
            print()


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