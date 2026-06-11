import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime


def scrape_jobs(keyword):
    """
    Scrape jobs from the website and filter by keyword.
    """

    url = "https://realpython.github.io/fake-jobs/"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"Error accessing website: {e}")
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

        if keyword.lower() not in title.lower():
            continue

        company = company_tag.text.strip() if company_tag else "N/A"
        location = location_tag.text.strip() if location_tag else "N/A"

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

    return jobs


def save_jobs(jobs, keyword):
    """
    Save jobs to CSV and Excel files.
    """

    df = pd.DataFrame(jobs)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    csv_file = f"{keyword}_{timestamp}.csv"
    excel_file = f"{keyword}_{timestamp}.xlsx"

    df.to_csv(csv_file, index=False)
    df.to_excel(excel_file, index=False)

    print("\nFILES CREATED")
    print("-" * 40)
    print(csv_file)
    print(excel_file)

    return csv_file, excel_file


def show_summary(jobs, keyword):
    """
    Display summary statistics.
    """

    print("\nSCRAPING SUMMARY")
    print("-" * 40)

    print(f"Keyword searched : {keyword}")
    print(f"Jobs found       : {len(jobs)}")

    companies = {job["company"] for job in jobs}

    print(f"Unique companies : {len(companies)}")

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
    print("JOB SCRAPER")
    print("=" * 50)

    keyword = input("Enter keyword: ").strip()

    if not keyword:
        print("Keyword cannot be empty.")
        return

    jobs = scrape_jobs(keyword)

    if not jobs:
        print(f"No jobs found matching '{keyword}'")
        return

    save_jobs(jobs, keyword)

    show_summary(jobs, keyword)


if __name__ == "__main__":
    main()