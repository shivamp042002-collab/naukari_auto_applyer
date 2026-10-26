
import re

ALLOWED_LOCATIONS = [
    "mumbai",
    "navi mumbai",
    "thane",
    "remote",
]

ROLE_KEYWORDS = [
    "python",
    "django",
    "backend",
    "back-end",
    "junior software developer",
    "software engineer",
    "software developer",
]

def is_relevant(job):
    title = job.get("title", "").lower()
    url = job.get("url", "").lower()

    # Check the role
    if not any(keyword in title for keyword in ROLE_KEYWORDS):
        return False

    # Check the location from the job URL
    if not any(location in url for location in ALLOWED_LOCATIONS):
        return False

    # Reject explicit experience ranges above 1 year.
    # This is a preliminary check, not a reliable eligibility decision.
    match = re.search(r"-(\d+)-to-(\d+)-years", url)

    if match:
        min_years = int(match.group(1))
        max_years = int(match.group(2))

        if min_years > 0 or max_years > 1:
            return False

    return True


def filter_jobs(jobs):
    return [job for job in jobs if is_relevant(job)]
