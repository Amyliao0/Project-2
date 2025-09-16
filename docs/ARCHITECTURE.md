# ARCHITECTURE.md

## 1. System Overview

This project implements a **Hiring Trends Radar** by scraping public job postings from **Greenhouse-hosted startup boards**.  

The design is guided by three goals:
1. **Reliability** – handle common scraping failures gracefully.  
2. **Ethics** – respect server load and avoid collecting personal data.  
3. **Extensibility** – make it easy to add new startups or filter by industry.

---

## 2. Repository Structure

```text

project-name/
├── src/
│ ├── scraper.py # Main scraping logic (Greenhouse API + catalog integration)
│ ├── validators.py # Data validation rules
│ ├── transformers.py # Transformation pipeline for raw job records
├── docs/
│ ├── BUSINESS_CASE.md # Market analysis and pricing
│ ├── ETHICS.md # Ethical/legal considerations
│ ├── ARCHITECTURE.md # Technical design decisions
│ ├── AI_USAGE.md # Documentation of AI tool collaboration
├── data/
│ ├── startups.csv # Catalog of startups (name, industry, url)
│ └── sample_output.json # Example of processed data
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 3. Key Components

### 3.1 Scraper (`scraper.py`)
- **Input:**  
  - `--urls`: Explicit Greenhouse board URLs (e.g., `https://boards.greenhouse.io/anthropic`).  
  - `--industry`: Industry filter to load relevant URLs from `data/startups.csv`.  

- **Process:**  
  - **Greenhouse API call:**  
    Uses `https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true`.  
  - **Validation:**  
    Each record is passed through `validate_record()` (title, URL, location, date must be non-empty).  
  - **Transformation:**  
    Jobs normalized into consistent schema (`transform()`), ready for analytics.  

- **Output:**  
  JSON file (`data/output.json`) containing validated job postings.

---

### 3.2 Catalog (Industry Filtering)
- **File:** `data/startups.csv`  
- **Format:** `name,industry,url`  
- **Purpose:** Enables batch scraping by industry (`--industry ai` pulls all AI startups).  
- **Design choice:** Using a simple CSV makes the system transparent, editable by non-technical users, and easy to expand.

---

### 3.3 Resilience Features
- **Retry logic:** Implemented with `tenacity` (exponential backoff, jitter).  
- **Rate limiting:** Randomized `sleep()` delays between requests.  
- **Robots.txt checks:** Attempted before fetching; defaults to "allow" if file unavailable (to avoid false negatives).  
- **Safety cap:** `--max-per-site` argument prevents runaway scraping.

---

## 4. Design Decisions

1. **Greenhouse-only scope**  
   - Chosen for consistency: Greenhouse has a clean, public API.  
   - Reduces complexity compared to supporting multiple ATS providers (Lever, Ashby, Workday).  

2. **Catalog-based expansion**  
   - Instead of hardcoding companies, we maintain `startups.csv`.  
   - Users can easily add startups under categories like `ai`, `fintech`, or `health`.

3. **Validation and transformation layers**  
   - Separating validation (`validators.py`) and transformation (`transformers.py`) improves clarity.  
   - Keeps `scraper.py` focused on orchestration.  

4. **JSON as output format**  
   - Chosen for portability and structured analysis.  
   - Could easily be extended to CSV or database outputs later.  

---

## 5. Future Extensions

- **Analytics Layer:** Add scripts to compute hiring trends over time (growth in postings, sector comparisons).  
- **Visualization:** Dashboards for recruiters/investors to filter and view trends.  
- **Additional ATS Providers:** Reintroduce Lever/Ashby/Workday once Greenhouse version is stable.  
- **Scheduling:** Cron job or GitHub Actions for automatic weekly scraping.  

---

**Conclusion:**  
The scraper is deliberately lightweight but robust: it handles failures, avoids overloading servers, and outputs consistent job data. By focusing on Greenhouse and using an industry catalog, the architecture remains simple, transparent, and extensible.

