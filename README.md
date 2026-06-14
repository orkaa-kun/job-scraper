# Job Scraper

A Python-based job scraping tool that collects job listings from a website, filters results by keyword, and exports data to multiple formats.

## Features

- Scrapes job listings using `requests` and `BeautifulSoup`
- Filters jobs by keyword
- Extracts:
  - Job Title
  - Company Name
  - Location
  - Application Link
- Exports results to:
  - CSV
  - Excel (.xlsx)
  - JSON
- Generates timestamped output files
- Stores exports in a dedicated `output/` folder
- Displays summary statistics
- Shows top companies in the search results
- Handles network and request errors gracefully

---

## Technologies Used

- Python
- Requests
- BeautifulSoup4
- Pandas
- OpenPyXL

---

## Project Structure

```text
job-scraper/
│
├── output/
│   ├── Python_2026-06-12_04-57-47.csv
│   ├── Python_2026-06-12_04-57-47.xlsx
│   └── Python_2026-06-12_04-57-47.json
│
├── scraper.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/orkaa-kun/job-scraper.git
cd job-scraper
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

Run the scraper:

```bash
python scraper.py
```

Enter a keyword when prompted:

```text
Enter keyword: Python
```

Example output:

```text
==================================================
JOB SCRAPER
==================================================

Enter keyword: Python

FILES CREATED
----------------------------------------
output\Python_2026-06-12_04-57-47.csv
output\Python_2026-06-12_04-57-47.xlsx
output\Python_2026-06-12_04-57-47.json

SCRAPING SUMMARY
----------------------------------------
Keyword searched : Python
Jobs found       : 10
Unique companies : 10
```

---

## Data Collected

Each job record contains:

| Field | Description |
|---------|---------|
| Title | Job title |
| Company | Company name |
| Location | Job location |
| Apply Link | Application URL |

---

## Example JSON Output

```json
{
    "title": "Software Developer (Python)",
    "company": "Adams-Brewer",
    "location": "Brockburgh, AE",
    "apply_link": "https://example.com"
}
```

---

## Learning Objectives

This project was built to practice:

- Web scraping
- HTML parsing
- Data extraction
- Data cleaning
- File exports
- Error handling
- Git and GitHub workflow
- Python project organization

---

## Future Improvements

- Command-line arguments
- Multiple website support
- Selenium integration
- Playwright integration
- Database storage
- Scheduled scraping

---

## Author

**Orka Dasgupta**

GitHub: https://github.com/orkaa-kun