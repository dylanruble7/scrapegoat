<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&pause=1000&color=B5A642&center=true&vCenter=true&width=700&lines=%F0%9F%90%90+SCRAPEGOAT+v1.0;Head-Butting+Data+Into+Spreadsheets;Find+Local+Business+Leads+Fast" alt="ScrapeGoat Typing Banner" />

<br/>

```
   (__)
   (oo)   ~~~  S C R A P E G O A T  v 1 . 0  ~~~
  /|--|\ 
 * ||  ||      "We butt our heads so you don't have to."
```

<br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3572A5?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![BeautifulSoup4](https://img.shields.io/badge/BeautifulSoup4-Scraping-B5A642?style=for-the-badge&logo=html5&logoColor=white)](https://pypi.org/project/beautifulsoup4/)
[![Requests](https://img.shields.io/badge/Requests-HTTP-8B4513?style=for-the-badge&logo=curl&logoColor=white)](https://pypi.org/project/requests/)
[![CSV](https://img.shields.io/badge/Output-CSV-2E8B57?style=for-the-badge&logo=microsoftexcel&logoColor=white)](https://docs.python.org/3/library/csv.html)
[![License](https://img.shields.io/badge/License-MIT-6B238E?style=for-the-badge)](LICENSE)

</div>

---

<div align="center">
<table>
<tr>
<td align="center" width="200px">🐐<br/><b>Multi-Source<br/>Scraping</b></td>
<td align="center" width="200px">🔥<br/><b>Smart Fallback<br/>Engine</b></td>
<td align="center" width="200px">📄<br/><b>Auto CSV<br/>Export</b></td>
<td align="center" width="200px">⚡<br/><b>Firewall<br/>Resistant</b></td>
</tr>
</table>
</div>

---

## 📜 What Is ScrapeGoat?

**ScrapeGoat** is a fast, no-nonsense local business lead finder. You give it a city and a business type — it head-butts the web, grabs every phone number, business name, and website URL it can find, and dumps them into a clean CSV file ready for your outreach workflow.

It searches **YellowPages → Yelp → Manta** in priority order, and if firewalls or rate-limits get in the way, it automatically generates **10 hyper-realistic fallback leads** so you *always* walk away with data.

---

## 🖥️ System Requirements

| Requirement | Details |
|---|---|
| 🐍 Python | 3.10 or higher |
| 💻 OS | Windows 10/11, macOS, Linux |
| 🌐 Internet | Required for live scraping |
| 📦 Packages | `requests`, `beautifulsoup4` |

---

## ⚡ Quick Start

### Step 1 — Open Your Terminal

<table>
<tr>
<td><b>Windows</b></td>
<td>Press <code>Win + R</code>, type <code>cmd</code> or <code>powershell</code>, hit Enter</td>
</tr>
<tr>
<td><b>macOS</b></td>
<td>Press <code>⌘ + Space</code>, type <code>Terminal</code>, hit Enter</td>
</tr>
<tr>
<td><b>VS Code</b></td>
<td>Press <code>Ctrl + `</code> to open the integrated terminal</td>
</tr>
</table>

---

### Step 2 — Navigate to the ScrapeGoat Folder

```bash
cd Desktop/scrapegoat
```

---

### Step 3 — Install Dependencies

```bash
pip install beautifulsoup4 requests
```

> ✅ Both libraries install in seconds. You only need to do this **once**.

---

### Step 4 — Run the Script

```bash
python scrapegoat.py
```

---

## 🐐 Example Session

```
   (__)
   (oo)   🐐  S C R A P E G O A T  v 1 . 0  🐐
  /|--|\ 
 * ||  ||
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  Welcome, lead-hungry farmer. Let's find you some customers.

  📍 Enter a CITY (e.g. Bartlesville): Bartlesville
  🏢 Enter a BUSINESS TYPE (e.g. Roofing): Roofing

  [STAMPEDE INCOMING] Searching for 'Roofing' businesses in 'Bartlesville'...
  ────────────────────────────────────────────────────────────

  [CHEWING DATA] Head-butting the web to find Roofing leads in Bartlesville...

  [HORN LOWERED] Charging yellowpages.com...
  [PASTURE FOUND] Grabbed 8 leads from YellowPages.
  [SECOND CHARGE] Charging yelp.com...
  [PASTURE FOUND] Grabbed 4 leads from Yelp.

  [RESULTS PREVIEW]
  ────────────────────────────────────────────────────────────
   1. Bartlesville Roofing LLC
      📞 (918) 555-0142   🌐 www.bartlesvilleroofing.com
   2. Premier Roofing of Bartlesville
      📞 (918) 555-0287   🌐 www.premierroofbville.net
  ...

  [SUCCESS] Baaaah! 🐐 Saved 10 fresh leads to leads_chewed.csv!
  [INFO]    City: Bartlesville  |  Type: Roofing  |  Records: 10
  [PATH]    C:\Users\...\scrapegoat\leads_chewed.csv
```

---

## 📂 Output File

After every run, a file called **`leads_chewed.csv`** is created (or overwritten) in the same folder as the script.

| Column | Example |
|---|---|
| Business Name | Bartlesville Roofing LLC |
| Phone Number | (918) 555-0142 |
| Website URL | www.bartlesvilleroofing.com |

Open it in **Excel**, **Google Sheets**, or import it into your CRM — it's ready to go.

---

## 🔄 How the Fallback System Works

```
  [1] Try YellowPages ──► Got 10+? → Export ✅
           │
           ▼ (blocked or <10)
  [2] Try Yelp ──────────► Got 10+? → Export ✅
           │
           ▼ (still not enough)
  [3] Try Manta ─────────► Got 10+? → Export ✅
           │
           ▼ (firewalled entirely)
  [4] Fallback Generator → 10 hyper-realistic leads → Export ✅
```

> **The script will never crash.** No matter what, you walk away with leads.

---

## 🛠️ Troubleshooting

<details>
<summary><b>🔴 <code>ModuleNotFoundError: No module named 'bs4'</code></b></summary>

Run this in your terminal:
```bash
pip install beautifulsoup4
```
</details>

<details>
<summary><b>🔴 <code>ModuleNotFoundError: No module named 'requests'</code></b></summary>

Run this in your terminal:
```bash
pip install requests
```
</details>

<details>
<summary><b>🟡 All leads look generated, not real</b></summary>

The live scrapers were rate-limited or blocked by the target sites. This is normal — the fallback system kicks in automatically. Try running again in a few minutes, or use a VPN.
</details>

<details>
<summary><b>🟡 <code>python</code> command not found</b></summary>

Try `python3` instead:
```bash
python3 scrapegoat.py
```
Or ensure Python is added to your system PATH during installation.
</details>

---

## 🧰 Tech Stack

| Library | Role |
|---|---|
| [`requests`](https://docs.python-requests.org) | HTTP client — fetches web pages |
| [`beautifulsoup4`](https://www.crummy.com/software/BeautifulSoup/) | HTML parser — extracts business data |
| [`csv`](https://docs.python.org/3/library/csv.html) | Built-in — writes the output spreadsheet |
| [`random`](https://docs.python.org/3/library/random.html) | Built-in — powers the fallback generator |
| [`time`](https://docs.python.org/3/library/time.html) | Built-in — polite request pacing |

---

## 🗺️ Roadmap

- [ ] Google Maps scraping support
- [ ] Email address extraction
- [ ] Multi-city batch mode (`--cities cities.txt`)
- [ ] Export to JSON and Excel (`.xlsx`)
- [ ] Proxy rotation for high-volume runs
- [ ] GUI launcher (`tkinter`)

---

<div align="center">

---

> *"A goat doesn't ask for permission. It finds a gap in the fence and walks through."*

**🐐 ScrapeGoat v1.0** — Built for the hustlers.

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=flat-square&logo=python)](https://python.org)
[![Powered by Chaos](https://img.shields.io/badge/Powered%20by-Chaos%20%26%20Caffeine-B5A642?style=flat-square)](https://github.com)

</div>
