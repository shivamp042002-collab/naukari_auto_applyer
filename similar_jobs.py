
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from job_search_config import PREFERRED_ROLES, REFERENCE_JOB_URL

DRIVER_PATH = r"C:\Users\Shivam\Desktop\JobSailor-main\geckodriver.exe"
FIREFOX_PATH = r"C:\Program Files\Mozilla Firefox\firefox.exe"


def build_search_urls():
    roles = list(dict.fromkeys(PREFERRED_ROLES))
    return [
        f"https://www.naukri.com/{quote_plus(role).replace('+', '-')}-jobs"
        for role in roles
    ]


def extract_jobs(html):
    soup = BeautifulSoup(html, "html.parser")
    jobs = []
    seen = set()

    for link in soup.select("a[href*='job-listings-']"):
        href = link.get("href", "")
        title = link.get_text(" ", strip=True)

        if not href.startswith("http"):
            continue

        if "naukri.com" not in href:
            continue

        if href in seen or not title:
            continue

        seen.add(href)
        jobs.append({
            "title": title,
            "url": href.split("?")[0],
        })

    return jobs


if __name__ == "__main__":
    options = Options()
    options.binary_location = FIREFOX_PATH
    driver = webdriver.Firefox(
        service=Service(DRIVER_PATH),
        options=options,
    )

    try:
        urls = build_search_urls()
        print("Search URLs:")
        for index, url in enumerate(urls, start=1):
            print(f"{index}. {url}")

        driver.get(urls[0])
        input(
            "Inspect the search results in Firefox. "
            "When ready, press Enter in this terminal..."
        )

        jobs = extract_jobs(driver.page_source)
        print(f"\nExtracted {len(jobs)} possible job links:")

        for job in jobs[:20]:
            print(f"- {job['title']}\n  {job['url']}")

        if not jobs:
            print(
                "No links extracted. Naukri may have changed its page "
                "structure or rendered the listings differently."
            )
    finally:
        try:
            driver.quit()
        except Exception:
            pass
