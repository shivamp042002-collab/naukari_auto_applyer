
from urllib.parse import quote_plus
from job_search_config import PREFERRED_ROLES, PREFERRED_LOCATIONS


def build_search_urls(reference_title):
    """Build Naukri search URLs from the reference job title and preferences."""
    search_terms = list(dict.fromkeys(
        [reference_title] + PREFERRED_ROLES
    ))

    urls = []

    for term in search_terms:
        query = quote_plus(term)
        urls.append(
            f"https://www.naukri.com/{query.replace('+', '-')}-jobs"
        )

    return urls


if __name__ == "__main__":
    from job_search_config import REFERENCE_JOB_URL

    print("Reference job:", REFERENCE_JOB_URL)
    print("\nSearch URLs to review:\n")

    for url in build_search_urls("Software Engineer"):
        print(url)
