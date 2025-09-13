# ETHICS.md

## Respectful Scraping
- Honor `robots.txt` and site Terms.
- Rate-limit requests; avoid parallel hits to the same domain.
- Use clear `User-Agent` and contact email if permitted by policy.

## Data Minimization
Collect only public job listing data (title, location, URL, posting date). Avoid PII.

## Transparency
Document data sources, timestamps, and transformation steps in commits and PRs.

## Contested Areas
- When a site disallows scraping in `robots.txt`, **do not scrape**.
- When dynamic content requires login, **skip** (no authentication in MVP).
