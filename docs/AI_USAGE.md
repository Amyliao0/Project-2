# AI.USAGE.md
## 1. Prompts Used with AI Tools

These are the main prompts I used while developing the Greenhouse-only scraper with AI:

- "Write a Python scraper for Greenhouse job boards using requests + JSON API."
- "Add retry logic with exponential backoff and a custom user agent string."
- "Fix: my scraper is returning 0 items even when the Greenhouse board has open jobs."
- "Explain what Greenhouse is and why startups use it."

---

## 2. Code Attribution: AI vs Human

**AI-generated (initial draft):**
- `extract_greenhouse_api` function for Greenhouse API extraction
- Retry logic with `tenacity`.
- Initial `main()` loop writing out to `data/output.json`.
- Boilerplate argparse setup for `--urls` and `--out`.

**Human-written (my contributions):**
- Added `catalog.py` logic directly into the scraper (`load_catalog`, `urls_for_industry`).
- Integrated the `--industry` flag so I can scrape by industry instead of hardcoding URLs.
- Implemented URL de-duplication across catalog and command line inputs
- Adjusted the code to simplify around **only Greenhouse**, removing Lever/Ashby/Workday paths.

---

## 3. Bugs Found in AI Suggestions (and Fixes)


- **Bug 1: Empty output even when jobs existed**  
  - Some Greenhouse boards initially returned 0 items because the API path wasn’t constructed correctly.  
  - **Fix:** I double-checked the API format (`https://boards-api.greenhouse.io/v1/boards/<company>/jobs?content=true`) and corrected the string.

- **Bug 2: Robots.txt handling too strict**  
  - AI’s first version refused to scrape if robots.txt could not be fetched.  
  - **Fix:** I modified `can_fetch` so that if robots.txt is missing or unreadable, scraping defaults to allowed (only blocks if explicitly disallowed).

---

## 4. Performance Comparisons (If Tested)

- **Direct HTML scraping** (AI initially suggested as fallback) → slow, brittle, and often returned “NO ITEMS.”  
- **Using Greenhouse API** (final version) → consistent, fast, and jobs are structured JSON (title, location, date, URL).  
- **Catalog vs manual input:** Catalog saves effort by letting me type `--industry ai` instead of pasting URLs one by one.

---

## 5. Reflections

Using AI was useful for scaffolding (boilerplate code, retry logic, API calls). But I had to simplify and clean the scope to focus on Greenhouse only, fix syntactic and logical bugs, and integrate the catalog so that the project matches assignment requirements. The final scraper is much leaner and more reliable.
