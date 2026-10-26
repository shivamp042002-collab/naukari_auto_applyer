
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

from job_search_config import REFERENCE_JOB_URL
from job_analyzer import analyze_job_page
import time
driver_path = r"C:\Users\Shivam\Desktop\JobSailor-main\geckodriver.exe"
firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"

options = Options()
options.binary_location = firefox_path

driver = None

try:
    driver = webdriver.Firefox(
        service=Service(driver_path),
        options=options
    )

    driver.get(REFERENCE_JOB_URL)
    time.sleep(5)

    job = analyze_job_page(driver.page_source, driver.current_url)

    print("\n--- Reference Job Details ---")
    print("Title:", job["title"])
    print("Description preview:", job["description"][:1500])
    print("Description characters:", len(job["description"]))

finally:
    if driver:
        driver.quit()
