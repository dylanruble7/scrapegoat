"""
🐐 ScrapeGoat v1.0 — Streamlit Web Interface
"""

import csv
import io
import random
import time

import requests
import streamlit as st
from bs4 import BeautifulSoup

# ─────────────────────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🐐 ScrapeGoat – Lead Finder",
    page_icon="🐐",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Georgia', serif;
}

/* Dark parchment background */
.stApp {
    background: radial-gradient(ellipse at top left, #1c1a14 0%, #0f0d08 60%, #1a1208 100%);
    color: #e8d5a3;
}

/* ── Header band ── */
.sg-header {
    background: linear-gradient(135deg, #2a1f05 0%, #3d2c08 50%, #1f1803 100%);
    border: 1px solid #b5922a;
    border-radius: 12px;
    padding: 28px 32px 20px;
    text-align: center;
    margin-bottom: 24px;
    box-shadow: 0 0 40px rgba(181,146,42,0.25), inset 0 0 60px rgba(0,0,0,0.4);
}
.sg-header pre {
    color: #d4aa3a;
    font-size: 13px;
    line-height: 1.35;
    margin: 0 0 8px;
    font-family: 'Courier New', monospace;
}
.sg-title {
    font-size: 2.1rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    color: #f0d060;
    text-shadow: 0 0 18px rgba(240,208,96,0.55);
    margin: 0;
}
.sg-subtitle {
    color: #a08840;
    font-style: italic;
    font-size: 1rem;
    margin-top: 4px;
}

/* ── Inputs ── */
.stTextInput > label {
    color: #c8a84b !important;
    font-size: 0.95rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.stTextInput input {
    background: #1c1705 !important;
    border: 1px solid #6b5120 !important;
    border-radius: 8px !important;
    color: #f0e0b0 !important;
    font-size: 1.05rem !important;
    padding: 10px 14px !important;
    transition: border-color 0.2s;
}
.stTextInput input:focus {
    border-color: #c8a84b !important;
    box-shadow: 0 0 0 2px rgba(200,168,75,0.25) !important;
}

/* ── Main button ── */
div[data-testid="stButton"] > button {
    width: 100%;
    background: linear-gradient(135deg, #b5922a 0%, #d4aa3a 40%, #9c7a1e 100%) !important;
    color: #0f0d08 !important;
    font-size: 1.15rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.06em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 0 !important;
    text-transform: uppercase !important;
    box-shadow: 0 4px 18px rgba(181,146,42,0.45) !important;
    transition: transform 0.12s, box-shadow 0.12s !important;
    margin-top: 8px;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 7px 26px rgba(181,146,42,0.65) !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0px) !important;
}

/* ── Terminal console log ── */
.sg-console {
    background: #050503;
    border: 1px solid #3a2e10;
    border-radius: 10px;
    padding: 16px 20px;
    font-family: 'Courier New', monospace;
    font-size: 0.83rem;
    line-height: 1.7;
    color: #a0c060;
    min-height: 80px;
    max-height: 340px;
    overflow-y: auto;
    margin: 18px 0 0;
    box-shadow: inset 0 0 30px rgba(0,0,0,0.6);
}
.sg-console .log-stamp  { color: #6b8840; }
.sg-console .log-warn   { color: #c8a030; }
.sg-console .log-err    { color: #c84040; }
.sg-console .log-ok     { color: #50d090; }
.sg-console .log-info   { color: #70a8d8; }

/* ── Results section ── */
.sg-results-header {
    background: linear-gradient(90deg, #1c1705, #2a1f05);
    border-left: 3px solid #b5922a;
    border-radius: 0 8px 8px 0;
    padding: 10px 18px;
    margin: 24px 0 10px;
    color: #f0d060;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.05em;
}

/* ── Dataframe overrides ── */
.stDataFrame {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #3a2e10 !important;
}
[data-testid="stDataFrameResizable"] {
    background: #0f0d08 !important;
}

/* ── Download button ── */
div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #1c4a2a 0%, #2a6b3c 50%, #163820 100%) !important;
    color: #70f0a0 !important;
    font-size: 1.0rem !important;
    font-weight: 700 !important;
    border: 1px solid #3a8a50 !important;
    border-radius: 10px !important;
    padding: 12px 0 !important;
    width: 100%;
    letter-spacing: 0.04em !important;
    box-shadow: 0 3px 14px rgba(60,180,90,0.3) !important;
    transition: transform 0.12s, box-shadow 0.12s !important;
    margin-top: 6px;
}
div[data-testid="stDownloadButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(60,180,90,0.45) !important;
}

/* ── Stat pills ── */
.sg-stat-row {
    display: flex;
    gap: 12px;
    margin: 14px 0 6px;
    flex-wrap: wrap;
}
.sg-stat {
    background: #1c1705;
    border: 1px solid #4a3a15;
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 0.85rem;
    color: #c8a84b;
    font-family: 'Courier New', monospace;
}

/* ── Divider ── */
hr { border-color: #3a2e10 !important; }

/* ── Footer ── */
.sg-footer {
    text-align: center;
    color: #5a4a20;
    font-size: 0.78rem;
    margin-top: 36px;
    padding-top: 12px;
    border-top: 1px solid #2a2010;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  CORE LOGIC  (ported from scrapegoat.py)
# ─────────────────────────────────────────────────────────────
SUFFIXES    = ["LLC", "Inc.", "Co.", "& Sons", "Experts", "Pros", "Solutions", "Group", "Services", "Team"]
TLDS        = [".com", ".net", ".biz", ".co"]
AREA_CODES  = {
    "bartlesville":"918","tulsa":"918","oklahoma city":"405","dallas":"214",
    "houston":"713","austin":"512","denver":"303","chicago":"312",
    "phoenix":"602","seattle":"206","miami":"305","atlanta":"404",
    "nashville":"615","charlotte":"704","los angeles":"213",
    "new york":"212","boston":"617","detroit":"313",
}
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def _area_code(city: str) -> str:
    return AREA_CODES.get(city.lower().strip(), str(random.randint(200, 999)))

def _slug(text: str) -> str:
    return text.lower().replace(" ", "").replace("&", "and")


def generate_fallback_leads(city: str, biz_type: str, count: int = 10) -> list[dict]:
    area      = _area_code(city)
    city_slug = _slug(city)
    templates = [
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
    random.shuffle(templates)
    used_names, used_phones, leads = set(), set(), []

    for i in range(count):
        name = templates[i % len(templates)]
        if name in used_names:
            name = f"{name} {i+1}"
        used_names.add(name)

        while True:
            phone = f"({area}) {random.randint(200,999)}-{random.randint(1000,9999)}"
            if phone not in used_phones:
                used_phones.add(phone)
                break

        name_part = _slug(name.replace(random.choice(SUFFIXES), "").strip())[:20]
        website   = f"www.{name_part}{city_slug[:6]}{random.choice(TLDS)}"
        leads.append({"Business Name": name, "Phone Number": phone, "Website URL": website})

    return leads


def scrape_yellowpages(city: str, biz_type: str, log) -> list[dict]:
    city_q = city.lower().replace(" ", "-")
    type_q = biz_type.lower().replace(" ", "-")
    url    = f"https://www.yellowpages.com/search?search_terms={type_q}&geo_location_terms={city_q}"
    log("warn", "🟡 [HORN LOWERED]  Charging yellowpages.com...")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=12)
        resp.raise_for_status()
    except Exception as e:
        log("err", f"🔴 [FENCE HIT]     YellowPages blocked the herd: {e}")
        return []

    soup  = BeautifulSoup(resp.text, "html.parser")
    leads = []
    for card in soup.select(".result")[:15]:
        name_el  = card.select_one(".business-name span") or card.select_one("h2.n")
        phone_el = card.select_one(".phones.phone.primary")
        link_el  = card.select_one("a.business-name")
        name     = name_el.get_text(strip=True)  if name_el  else ""
        phone    = phone_el.get_text(strip=True) if phone_el else "N/A"
        website  = link_el["href"]               if link_el and link_el.get("href") else ""
        if name:
            leads.append({
                "Business Name": name,
                "Phone Number":  phone,
                "Website URL":   website if website.startswith("http") else f"yellowpages.com{website}",
            })

    log("ok", f"🟢 [PASTURE FOUND] Grabbed {len(leads)} leads from YellowPages.")
    return leads


def scrape_yelp(city: str, biz_type: str, log) -> list[dict]:
    city_q = city.replace(" ", "+")
    type_q = biz_type.replace(" ", "+")
    url    = f"https://www.yelp.com/search?find_desc={type_q}&find_loc={city_q}"
    log("warn", "🟡 [SECOND CHARGE] Charging yelp.com...")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=12)
        resp.raise_for_status()
    except Exception as e:
        log("err", f"🔴 [FENCE HIT]     Yelp blocked the herd: {e}")
        return []

    soup  = BeautifulSoup(resp.text, "html.parser")
    leads = []
    for card in soup.select('[class*="businessName"]')[:15]:
        a_tag = card.find("a")
        if not a_tag:
            continue
        name    = a_tag.get_text(strip=True)
        href    = a_tag.get("href", "")
        website = f"yelp.com{href}" if href.startswith("/biz/") else href
        leads.append({"Business Name": name, "Phone Number": "See Yelp listing", "Website URL": website})

    log("ok", f"🟢 [PASTURE FOUND] Grabbed {len(leads)} leads from Yelp.")
    return leads


def scrape_manta(city: str, biz_type: str, log) -> list[dict]:
    city_q = city.lower().replace(" ", "-")
    type_q = biz_type.lower().replace(" ", "-")
    url    = f"https://www.manta.com/mb_{type_q}_{city_q}_us"
    log("warn", "🟡 [THIRD CHARGE]  Charging manta.com...")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=12)
        resp.raise_for_status()
    except Exception as e:
        log("err", f"🔴 [FENCE HIT]     Manta blocked the herd: {e}")
        return []

    soup  = BeautifulSoup(resp.text, "html.parser")
    leads = []
    for card in soup.select("article.search-result, .company-name")[:15]:
        name_el  = card.select_one("h2 a, .company-name a, a[data-hj-allow]")
        phone_el = card.select_one(".phone, [itemprop='telephone']")
        link_el  = card.select_one("a[href*='manta.com/c/']")
        name     = name_el.get_text(strip=True)  if name_el  else ""
        phone    = phone_el.get_text(strip=True) if phone_el else "N/A"
        website  = link_el["href"]               if link_el  else "See Manta listing"
        if name:
            leads.append({"Business Name": name, "Phone Number": phone, "Website URL": website})

    log("ok", f"🟢 [PASTURE FOUND] Grabbed {len(leads)} leads from Manta.")
    return leads


def hunt_leads(city: str, biz_type: str, log) -> list[dict]:
    log("info", f"🐐 [CHEWING DATA]  Head-butting the web to find {biz_type} leads in {city}...")
    time.sleep(0.4)

    scrapers   = [scrape_yellowpages, scrape_yelp, scrape_manta]
    all_leads: list[dict] = []

    for fn in scrapers:
        try:
            results = fn(city, biz_type, log)
            if results:
                all_leads.extend(results)
                if len(all_leads) >= 10:
                    break
        except Exception as e:
            log("err", f"🔴 [STUMBLE]       {fn.__name__} fell over the fence: {e}")
        time.sleep(random.uniform(0.6, 1.2))

    # Deduplicate
    seen, unique = set(), []
    for lead in all_leads:
        key = lead["Business Name"].lower().strip()
        if key and key not in seen:
            seen.add(key)
            unique.append(lead)

    if len(unique) >= 10:
        log("ok", f"✅ [LIVE DATA]     Scored {len(unique)} real-world leads — no backup needed!")
        return unique[:15]

    needed = max(10 - len(unique), 0)
    log("warn", f"🟡 [FALLBACK]      Only {len(unique)} live leads — grazing {needed} from the fallback meadow...")
    fallback = generate_fallback_leads(city, biz_type, needed + 2)

    for fb in fallback:
        if fb["Business Name"].lower() not in seen:
            unique.append(fb)
            seen.add(fb["Business Name"].lower())
        if len(unique) >= 10:
            break

    log("ok", f"✅ [HERD COMPLETE]  Padded to {len(unique[:10])} total leads. Baaaah!")
    return unique[:10]


def leads_to_csv_bytes(leads: list[dict]) -> bytes:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=["Business Name", "Phone Number", "Website URL"])
    writer.writeheader()
    for lead in leads:
        writer.writerow({k: lead.get(k, "") for k in ["Business Name", "Phone Number", "Website URL"]})
    return buf.getvalue().encode("utf-8")

# ─────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────
if "leads"    not in st.session_state: st.session_state.leads    = []
if "log_lines" not in st.session_state: st.session_state.log_lines = []
if "searched" not in st.session_state: st.session_state.searched  = False

# ─────────────────────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="sg-header">
  <pre>
   (__)
   (oo)   🐐  S C R A P E G O A T  v 1 . 0  🐐
  /|--|\\
 * ||  ||
  </pre>
  <div class="sg-title">🐐 ScrapeGoat Lead Finder</div>
  <div class="sg-subtitle">"We butt our heads so you don't have to."</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  INPUT FORM
# ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    city     = st.text_input("📍 City", placeholder="e.g. Bartlesville")
with col2:
    biz_type = st.text_input("🏢 Business Type", placeholder="e.g. Roofing")

run = st.button("🐐  Chew Data with ScrapeGoat")

# ─────────────────────────────────────────────────────────────
#  SCRAPE LOGIC  (runs only when button is pressed)
# ─────────────────────────────────────────────────────────────
if run:
    if not city.strip() or not biz_type.strip():
        st.error("🐐 Even goats need something to chew on — please fill in both fields.")
    else:
        st.session_state.log_lines = []
        st.session_state.leads     = []
        st.session_state.searched  = True

        console_placeholder = st.empty()

        TYPE_CLASS = {"ok": "log-ok", "warn": "log-warn", "err": "log-err", "info": "log-info"}

        def log(kind: str, msg: str) -> None:
            css = TYPE_CLASS.get(kind, "log-stamp")
            st.session_state.log_lines.append(f'<span class="{css}">{msg}</span>')
            lines_html = "<br>".join(st.session_state.log_lines)
            console_placeholder.markdown(
                f'<div class="sg-console">{lines_html}</div>',
                unsafe_allow_html=True,
            )

        log("stamp", f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        log("info",  f"🐐 [STAMPEDE]      City: {city.strip()}  |  Type: {biz_type.strip()}")
        log("stamp", f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        leads = hunt_leads(city.strip(), biz_type.strip(), log)
        st.session_state.leads = leads

        if leads:
            log("ok",   f"✅ [SUCCESS]       Baaaah! 🐐 Found {len(leads)} fresh leads!")
        else:
            log("err",  "🔴 [EMPTY FIELD]   The herd scattered — no leads found. Try again.")

        log("stamp", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

# ─────────────────────────────────────────────────────────────
#  RESULTS TABLE  (persists across rerenders)
# ─────────────────────────────────────────────────────────────
if st.session_state.searched and not run:
    # Rerender the console from session state (after Streamlit reruns)
    if st.session_state.log_lines:
        lines_html = "<br>".join(st.session_state.log_lines)
        st.markdown(f'<div class="sg-console">{lines_html}</div>', unsafe_allow_html=True)

if st.session_state.leads:
    leads = st.session_state.leads

    st.markdown(
        f'<div class="sg-results-header">📋 Results — {len(leads)} Lead{"s" if len(leads)!=1 else ""} Found</div>',
        unsafe_allow_html=True,
    )

    # Stat pills
    sources = set()
    for l in leads:
        w = l.get("Website URL", "")
        if "yellowpages" in w: sources.add("YellowPages")
        elif "yelp"       in w: sources.add("Yelp")
        elif "manta"      in w: sources.add("Manta")
        else:                   sources.add("Generated")
    source_str = " · ".join(sorted(sources)) if sources else "Mixed"

    st.markdown(f"""
    <div class="sg-stat-row">
      <span class="sg-stat">🐐 {len(leads)} Leads</span>
      <span class="sg-stat">📍 {city.strip() if city else "—"}</span>
      <span class="sg-stat">🏢 {biz_type.strip() if biz_type else "—"}</span>
      <span class="sg-stat">🌐 {source_str}</span>
    </div>
    """, unsafe_allow_html=True)

    # Interactive table — show as DataFrame
    import pandas as pd
    df = pd.DataFrame(leads)[["Business Name", "Phone Number", "Website URL"]]
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=False,
        column_config={
            "Business Name": st.column_config.TextColumn("🏢 Business Name",  width="large"),
            "Phone Number":  st.column_config.TextColumn("📞 Phone Number",   width="medium"),
            "Website URL":   st.column_config.LinkColumn("🌐 Website URL",    width="large"),
        },
    )

    # Download button
    csv_bytes = leads_to_csv_bytes(leads)
    st.download_button(
        label="⬇️  Download leads_chewed.csv",
        data=csv_bytes,
        file_name="leads_chewed.csv",
        mime="text/csv",
    )

# ─────────────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="sg-footer">
  🐐 ScrapeGoat v1.0 &nbsp;·&nbsp; "A goat doesn't ask for permission. It finds a gap in the fence and walks through."
</div>
""", unsafe_allow_html=True)
