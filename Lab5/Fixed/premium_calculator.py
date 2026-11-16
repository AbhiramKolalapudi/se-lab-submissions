
"""Calculate insurance premiums and manage policy quotes securely."""

import hmac
import math
import os
import secrets
import tarfile
import urllib.parse
import urllib.request
from datetime import date, datetime
from pathlib import Path
from typing import Optional

from defusedxml import ElementTree as ET

quotes = {}
HOST = os.getenv("PREMIUM_HOST", "127.0.0.1")
UNDERWRITER_TOKEN = os.getenv("UNDERWRITER_TOKEN", "")
LOG_FILE = Path(
    os.getenv("PREMIUM_LOG_FILE", str(Path.home() / "premium_quotes.log"))
)
BASE_RATES = {"health": 5000, "motor": 3000, "life": 8000}


def calculate_premium(
    policy_type,
    age,
    sum_insured,
    smoker,
    claims,
    discounts: Optional[list] = None,
):
    """Calculate a premium using policy details and optional discounts."""
    if policy_type not in BASE_RATES:
        raise ValueError(f"Unsupported policy type: {policy_type}")
    if age < 0 or sum_insured < 0 or claims < 0:
        raise ValueError(
            "Age, sum insured, and claims must be non-negative"
        )

    premium = BASE_RATES[policy_type] + sum_insured * 0.002
    if age > 45:
        premium *= 1.5
    if smoker:
        premium *= 1.3

    premium += claims * 1000
    for discount in discounts or []:
        if discount < 0:
            raise ValueError("Discounts must be non-negative")
        premium -= discount

    return max(0.0, premium)


def age_from_dob(dob):
    """Calculate a person's age from a date in DD-MM-YYYY format."""
    born = datetime.strptime(dob, "%d-%m-%Y").date()
    today = date.today()
    age = today.year - born.year

    if (today.month, today.day) < (born.month, born.day):
        age -= 1
    if age < 0:
        raise ValueError("Date of birth cannot be in the future")

    return age


def policy_number():
    """Generate a six-digit policy number with a POL prefix."""
    return f"POL-{secrets.randbelow(900000) + 100000}"


def save_quote(name, premium):
    """Save a quote in memory and append it to the quote log."""
    number = policy_number()
    quotes[number] = {"name": name, "premium": premium}
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with LOG_FILE.open("a", encoding="utf-8") as quote_file:
        quote_file.write(f"{number},{name},{premium:.2f}\n")

    return number


def import_policies(xml_text):
    """Parse valid policy records from XML, skipping invalid entries."""
    root = ET.fromstring(xml_text)
    result = []

    for policy in root.findall("policy"):
        try:
            policy_type = policy.get("type")
            age = int(policy.get("age", ""))
            sum_insured = int(policy.get("sum", ""))

            if (
                policy_type not in BASE_RATES
                or age < 0
                or sum_insured < 0
            ):
                continue

            result.append((policy_type, age, sum_insured))
        except (TypeError, ValueError):
            continue

    return result


def fetch_rates(url):
    """Download rate data from a valid HTTPS URL."""
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.scheme != "https" or not parsed_url.hostname:
        raise ValueError("Rate URL must be a valid HTTPS URL")

    # HTTPS uses Python's default certificate and hostname verification.
    # B310 may still flag urlopen; the scheme is explicitly validated.
    with urllib.request.urlopen(url, timeout=10) as response:  # nosec B310
        return response.read()


def import_claim_documents(archive_path):
    """Safely extract supported files from a claims TAR archive."""
    destination = Path("claims_docs").resolve()
    destination.mkdir(parents=True, exist_ok=True)

    with tarfile.open(archive_path, "r:*") as archive:
        for member in archive.getmembers():
            target = (destination / member.name).resolve()

            if target != destination and destination not in target.parents:
                raise ValueError(f"Unsafe archive path: {member.name}")

            if member.issym() or member.islnk() or member.isdev():
                raise ValueError(
                    f"Unsupported archive member: {member.name}"
                )

        archive.extractall(destination, filter="data")


def monthly_instalment(premium, months=12):
    """Calculate the whole-unit monthly premium instalment."""
    if months <= 0:
        raise ValueError("Months must be greater than zero")

    return math.floor(premium / months)


def is_authorised(token):
    """Check an underwriter token using a constant-time comparison."""
    if not UNDERWRITER_TOKEN:
        return False

    return hmac.compare_digest(str(token), UNDERWRITER_TOKEN)


def renewal_due(start, years=1):
    """Calculate a renewal date, using February 28 for leap-day edge cases."""
    start_date = datetime.strptime(start, "%Y-%m-%d").date()

    try:
        renewal_date = start_date.replace(year=start_date.year + years)
    except ValueError:
        renewal_date = start_date.replace(
            year=start_date.year + years,
            month=2,
            day=28,
        )

    return renewal_date.strftime("%Y-%m-%d")


def print_quotes():
    """Print all quotes currently stored in the quote book."""
    print("===== Quote Book =====")
    for index, (number, quote) in enumerate(quotes.items(), start=1):
        print(index, number, quote["name"], "Rs.", quote["premium"])


def main():
    """Run sample calculations and demonstrate the calculator features."""
    premium_one = calculate_premium("health", 30, 500000, False, 0)
    premium_two = calculate_premium("health", 30, 500000, False, 0)
    premium_three = calculate_premium("motor", 50, 800000, False, 0)
    premium_four = calculate_premium(
        "life", 25, 100000, False, 0, [3000, 3000, 3000]
    )

    print("Quote 1:", premium_one)
    print("Quote 2 (same customer details):", premium_two)
    print("Non-smoker aged 50:", premium_three)
    print("Life with stacked discounts:", premium_four)
    print("Age from DOB 31-12-1990:", age_from_dob("31-12-1990"))
    print("Monthly instalment:", monthly_instalment(premium_three))
    print("Renewal due:", renewal_due("2025-03-15"))

    sample_xml = (
        "<policies><policy type='health' age='40' sum='300000'/>"
        "<policy type='motor' age='abc' sum='1'/></policies>"
    )
    print("Imported:", import_policies(sample_xml))
    print("Saved as:", save_quote("Kiran", premium_one))
    print("Authorised:", is_authorised(os.getenv("UNDERWRITER_TOKEN", "")))
    print("Server would listen on", HOST)
    print_quotes()


if __name__ == "__main__":
    main()
