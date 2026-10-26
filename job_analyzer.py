
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re


def analyze_job_page(html, url):
    """Extract basic job details from a Naukri job page."""
    parsed_url = urlparse(url)

    if parsed_url.netloc.lower() not in {
        "naukri.com",
        "www.naukri.com",
    }:
        raise ValueError("Please provide a valid Naukri job URL.")

    soup = BeautifulSoup(html, "html.parser")

    # Extract the page title
    title = soup.title.get_text(" ", strip=True) if soup.title else ""

    # Try common job-description containers
    description_selectors = [
        ".styles_JDC__dang-inner-html__h0K4t",
        ".job-desc",
        ".jd-desc",
        "#jobDescriptionText",
    ]

    description = ""
    for selector in description_selectors:
        element = soup.select_one(selector)
        if element:
            description = element.get_text(" ", strip=True)
            break

    # Fallback to visible page text if the description selector changes
    if not description:
        description = soup.get_text(" ", strip=True)

    # Keep the text manageable
    description = re.sub(r"\s+", " ", description).strip()[:12000]

    return {
        "url": url,
        "title": title,
        "description": description,
    }
