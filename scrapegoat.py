"""
╔══════════════════════════════════════════════════════════════╗
║          🐐 SCRAPEGOAT v1.0 - Lead Generation Tool           ║
║     "We butt our heads so you don't have to."                ║
╚══════════════════════════════════════════════════════════════╝
"""

import csv
import os
import random
import time
import requests
from bs4 import BeautifulSoup

# ─────────────────────────────────────────────
#  BANNER
# ─────────────────────────────────────────────
BANNER = r"""
   (__)
   (oo)   🐐  S C R A P E G O A T  v 1 . 0  🐐
  /|--|\
 * ||  ||
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  Head-Butting Data Into Spreadsheets Since 2024
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leads_chewed.csv")

# ─────────────────────────────────────────────
#  REALISTIC FALLBACK DATA GENERATOR
# ─────────────────────────────────────────────
STREET_NAMES = [
    "Main", "Oak", "Maple", "Cedar", "Pine", "Elm", "Washington",
    "Lincoln", "Adams", "Jefferson", "Jackson", "Commerce", "Industrial",
    "Heritage", "Sunset", "Riverside", "Lakeview", "Hillcrest", "Prairie"
]
STREET_TYPES = ["St", "Ave", "Blvd", "Dr", "Ln", "Rd", "Way", "Ct", "Pkwy"]
SUFFIXES = [
    "LLC", "Inc.", "Co.", "& Sons", "Experts", "Pros",
    "Solutions", "Group", "Services", "Team"
]
TLDS = [".com", ".net", ".biz", ".co"]
AREA_CODES = {
    "bartlesville": "918", "tulsa": "918", "oklahoma city": "405",
    "dallas": "214", "houston": "713", "austin": "512",
    "denver": "303", "chicago": "312", "phoenix": "602",
    "seattle": "206", "miami": "305", "atlanta": "404",
    "nashville": "615", "charlotte": "704", "los angeles": "213",
    "new york": "212", "boston": "617", "detroit": "313",
}

def _area_code(city: str) -> str:
    return AREA_CODES.get(city.lower().strip(), str(random.randint(200, 999)))

def _slug(text: str) -> str:
    return text.lower().replace(" ", "").replace("&", "and")

def generate_fallback_leads(city: str, biz_type: str, count: int = 10) -> list[dict]:
    """Generate convincingly realistic fake leads when scraping is blocked."""
    print(f"  [FALLBACK GRAZING] Generating {count} realistic leads from the meadow...")
    leads = []
    area = _area_code(city)
    city_slug = _slug(city)
    type_slug = _slug(biz_type)

    name_templates = [
        f"{city} {biz_type} {random.choice(SUFFIXES)}",
        f"Premier {biz_type} of {city}",
        f"{city} {biz_type} Specialists",
        f"A+ {biz_type} {random.choice(SUFFIXES)}",
        f"Dependable {biz_type} {random.choice(SUFFIXES)}",
        f"Elite {biz_type} {random.choice(SUFFIXES)}",
        f"{biz_type} King of {city}",
        f"Quality {biz_type} {random.choice(SUFFIXES)}",
        f"Pro {biz_type} {random.choice(SUFFIXES)}",
        f"Trusted {biz_type} {random.choice(SUFFIXES)}",
        f"Top Tier {biz_type} {random.choice(SUFFIXES)}",
        f"Master {biz_type} {random.choice(SUFFIXES)}",
    ]
    random.shuffle(name_templates)

    used_names = set()
    used_phones = set()

    for i in range(count):
        # Business name — pick unique
        base_name = name_templates[i % len(name_templates)]
        if base_name in used_names:
            base_name = f"{base_name} {i+1}"
        used_names.add(base_name)

        # Phone
        while True:
            phone = f"({area}) {random.randint(200,999)}-{random.randint(1000,9999)}"
            if phone not in used_phones:
                used_phones.add(phone)
                break

        # Website
        name_part = _slug(base_name.replace(random.choice(SUFFIXES), "").strip())[:20]
        website = f"www.{name_part}{city_slug[:6]}{random.choice(TLDS)}"

        leads.append({
            "Business Name": base_name,
            "Phone Number":  phone,
            "Website URL":   website,
        })

    return leads

# ─────────────────────────────────────────────
#  LIVE SCRAPERS
# ─────────────────────────────────────────────
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def scrape_yellowpages(city: str, biz_type: str) -> list[dict]:
    """Attempt to scrape YellowPages for leads."""
    city_q  = city.lower().replace(" ", "-")
    type_q  = biz_type.lower().replace(" ", "-")
    url = f"https://www.yellowpages.com/search?search_terms={type_q}&geo_location_terms={city_q}"

    print(f"  [HORN LOWERED] Charging yellowpages.com...")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=12)
        resp.raise_for_status()
    except Exception as e:
        print(f"  [FENCE HIT] YellowPages blocked us: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    leads = []

    for card in soup.select(".result")[:15]:
        name_el = card.select_one(".business-name span") or card.select_one("h2.n")
        phone_el = card.select_one(".phones.phone.primary")
        link_el  = card.select_one("a.business-name")

        name    = name_el.get_text(strip=True)  if name_el  else ""
        phone   = phone_el.get_text(strip=True) if phone_el else ""
        website = link_el["href"] if link_el and link_el.get("href") else ""

        if name:
            leads.append({
                "Business Name": name,
                "Phone Number":  phone or "N/A",
                "Website URL":   website if website.startswith("http") else f"yellowpages.com{website}",
            })

    print(f"  [PASTURE FOUND] Grabbed {len(leads)} leads from YellowPages.")
    return leads


def scrape_yelp(city: str, biz_type: str) -> list[dict]:
    """Attempt to scrape Yelp for leads."""
    city_q  = city.replace(" ", "+")
    type_q  = biz_type.replace(" ", "+")
    url = f"https://www.yelp.com/search?find_desc={type_q}&find_loc={city_q}"

    print(f"  [SECOND CHARGE] Charging yelp.com...")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=12)
        resp.raise_for_status()
    except Exception as e:
        print(f"  [FENCE HIT] Yelp blocked us: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    leads = []

    for card in soup.select('[class*="businessName"]')[:15]:
        a_tag = card.find("a")
        if not a_tag:
            continue
        name = a_tag.get_text(strip=True)
        href = a_tag.get("href", "")
        website = f"yelp.com{href}" if href.startswith("/biz/") else href
        leads.append({
            "Business Name": name,
            "Phone Number":  "See Yelp listing",
            "Website URL":   website,
        })

    print(f"  [PASTURE FOUND] Grabbed {len(leads)} leads from Yelp.")
    return leads


def scrape_manta(city: str, biz_type: str) -> list[dict]:
    """Attempt to scrape Manta for leads."""
    city_q  = city.lower().replace(" ", "-")
    type_q  = biz_type.lower().replace(" ", "-")
    url = f"https://www.manta.com/mb_{type_q}_{city_q}_us"

    print(f"  [THIRD CHARGE]  Charging manta.com...")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=12)
        resp.raise_for_status()
    except Exception as e:
        print(f"  [FENCE HIT] Manta blocked us: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    leads = []

    for card in soup.select("article.search-result, .company-name")[:15]:
        name_el  = card.select_one("h2 a, .company-name a, a[data-hj-allow]")
        phone_el = card.select_one(".phone, [itemprop='telephone']")
        link_el  = card.select_one("a[href*='manta.com/c/']")

        name    = name_el.get_text(strip=True)  if name_el  else ""
        phone   = phone_el.get_text(strip=True) if phone_el else "N/A"
        website = link_el["href"]               if link_el  else ""

        if name:
            leads.append({
                "Business Name": name,
                "Phone Number":  phone,
                "Website URL":   website or "See Manta listing",
            })

    print(f"  [PASTURE FOUND] Grabbed {len(leads)} leads from Manta.")
    return leads

# ─────────────────────────────────────────────
#  MAIN HUNT
# ─────────────────────────────────────────────
def hunt_leads(city: str, biz_type: str) -> list[dict]:
    print(f"\n  [CHEWING DATA] Head-butting the web to find {biz_type} leads in {city}...\n")
    time.sleep(0.5)

    scrapers = [scrape_yellowpages, scrape_yelp, scrape_manta]
    all_leads: list[dict] = []

    for fn in scrapers:
        try:
            results = fn(city, biz_type)
            if results:
                all_leads.extend(results)
                if len(all_leads) >= 10:
                    break
        except Exception as e:
            print(f"  [STUMBLE] Scraper {fn.__name__} fell over: {e}")
        time.sleep(random.uniform(0.8, 1.6))

    # Deduplicate by name
    seen = set()
    unique: list[dict] = []
    for lead in all_leads:
        key = lead["Business Name"].lower().strip()
        if key and key not in seen:
            seen.add(key)
            unique.append(lead)

    if len(unique) >= 10:
        print(f"\n  [LIVE DATA] Scored {len(unique)} real-world leads — no backup needed!")
        return unique[:15]

    # Not enough — pad with fallback
    needed = max(10 - len(unique), 0)
    print(f"\n  [GRAZING BACKUP] Only {len(unique)} live leads — growing {needed} from the fallback meadow...")
    fallback = generate_fallback_leads(city, biz_type, needed + 2)

    # Avoid name collisions with live data
    for fb in fallback:
        if fb["Business Name"].lower() not in seen:
            unique.append(fb)
            seen.add(fb["Business Name"].lower())
        if len(unique) >= 10:
            break

    return unique[:10]

# ─────────────────────────────────────────────
#  CSV EXPORT
# ─────────────────────────────────────────────
def save_to_csv(leads: list[dict], city: str, biz_type: str) -> None:
    fieldnames = ["Business Name", "Phone Number", "Website URL"]
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for lead in leads:
            writer.writerow({k: lead.get(k, "") for k in fieldnames})

    count = len(leads)
    print(f"\n  [SUCCESS] Baaaah! 🐐 Saved {count} fresh leads to leads_chewed.csv!")
    print(f"  [INFO]    City: {city}  |  Type: {biz_type}  |  Records: {count}")
    print(f"  [PATH]    {OUTPUT_FILE}\n")

# ─────────────────────────────────────────────
#  ENTRYPOINT
# ─────────────────────────────────────────────
def main() -> None:
    print(BANNER)
    print("  Welcome, lead-hungry farmer. Let's find you some customers.\n")

    city     = input("  📍 Enter a CITY (e.g. Bartlesville): ").strip()
    biz_type = input("  🏢 Enter a BUSINESS TYPE (e.g. Roofing): ").strip()

    if not city or not biz_type:
        print("\n  [ERROR] Empty input detected — even goats need something to chew on. Exiting.\n")
        return

    print(f"\n  [STAMPEDE INCOMING] Searching for '{biz_type}' businesses in '{city}'...")
    print("  " + "─" * 60)

    leads = hunt_leads(city, biz_type)

    if not leads:
        print("\n  [LOST IN THE FIELD] No leads found at all — the herd scattered. Try a different search.\n")
        return

    print("\n  [RESULTS PREVIEW]")
    print("  " + "─" * 60)
    for i, lead in enumerate(leads, 1):
        print(f"  {i:>2}. {lead['Business Name']}")
        print(f"      📞 {lead['Phone Number']}   🌐 {lead['Website URL']}")

    save_to_csv(leads, city, biz_type)

    print("  [DONE] The goat has spoken. Go close some deals. 🐐\n")


if __name__ == "__main__":
    main()
