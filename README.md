# Startup Hiring Radar

A minimal, **respectful** web scraper that aggregates open job roles from startup career pages (e.g., Greenhouse, Lever, Ashby, Workday) and produces a normalized JSON for downstream analysis.

> Built to align with the course requirements: data quality assurance, respectful scraping (exponential backoff + retry limits), and business logic transformations.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate  # on macOS/Linux
pip install -r requirements.txt

# Example: scrape a couple of known Greenhouse/Lever pages
python src/scraper.py --urls https://boards.greenhouse.io/openai                        https://jobs.lever.co/Notion
# Output will be written to data/output.json
```

## Repo Structure
```
project-name/
├── src/
│   ├── scraper.py          # Main scraping logic
│   ├── validators.py       # Data validation rules
│   ├── transformers.py     # Data transformation pipeline
├── docs/
│   ├── BUSINESS_CASE.md    # Market analysis and pricing
│   ├── ETHICS.md           # Detailed ethical analysis
│   ├── ARCHITECTURE.md     # Technical design decisions
│   ├── AI_USAGE.md         # AI collaboration documentation
├── data/
│   └── sample_output.json  # Example of processed data
├── requirements.txt
├── README.md
└── .gitignore
```

## Notes
- Always check `robots.txt` for each domain before scraping.
- This project intentionally **skips** JS-heavy sites for the MVP.
- You can extend `src/scraper.py` with new extractors for additional ATS patterns.
