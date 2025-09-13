#!/usr/bin/env python3
import argparse, json, random, time, urllib.parse, urllib.robotparser
from typing import Optional, Iterable

import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

from validators import validate_record
from transformers import transform

BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
API_UA = "StartupHiringRadar/0.1 (+contact: your-email@example.com)"

def can_fetch(url: str, user_agent: str = BROWSER_UA) -> bool:
    parsed = urllib.parse.urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = urllib.robotparser.RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception:
        # If robots can't be fetched, be conservative and skip
        return False

@retry(wait=wait_exponential_jitter(exp_base=2, max=10), stop=stop_after_attempt(3))
def fetch_html(url: str, session: Optional[requests.Session] = None) -> requests.Response:
    sess = session or requests.Session()
    headers = {"User-Agent": BROWSER_UA, "Accept": "text/html,application/xhtml+xml"}
    resp = sess.get(url, headers=headers, timeout=20, allow_redirects=True)
    resp.raise_for_status()
    time.sleep(1 + random.random())
    return resp

@retry(wait=wait_exponential_jitter(exp_base=2, max=10), stop=stop_after_attempt(3))
def fetch_json(url: str, session: Optional[requests.Session] = None) -> requests.Response:
    sess = session or requests.Session()
    headers = {"User-Agent": API_UA, "Accept": "application/json"}
    resp = sess.get(url, headers=headers, timeout=20)
    resp.raise_for_status()
    time.sleep(1 + random.random())
    return resp

# ---------------- Provider detectors ----------------

def is_greenhouse(url: str) -> bool:
    return "greenhouse.io" in url

def is_lever(url: str) -> bool:
    host = urllib.parse.urlparse(url).netloc
    return "lever.co" in host

def guess_company_from_url(url: str) -> Optional[str]:
    # GH: https://boards.greenhouse.io/openai
    # Lever: https://jobs.lever.co/notion
    path = urllib.parse.urlparse(url).path.strip("/")
    if not path:
        return None
    # company is typically the first segment
    return path.split("/")[0].lower()

# ---------------- Greenhouse via API ----------------

def extract_greenhouse_api(company: str, session: Optional[requests.Session] = None):
    api = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true"
    try:
        data = fetch_json(api, session).json()
    except Exception as e:
        print(f"[GH API ERROR] {company}: {e}")
        return []

    out = []
    for j in data.get("jobs", []):
        title = j.get("title") or ""
        url = j.get("absolute_url") or ""
        loc = (j.get("location") or {}).get("name")
        date = j.get("updated_at") or j.get("created_at")
        out.append({
            "title": title,
            "location": loc,
            "date": date,
            "url": url,
            "source": "greenhouse",
            "company": company.title(),
        })
    return out

# ---------------- Lever via API ----------------

def extract_lever_api(company: str, session: Optional[requests.Session] = None):
    api = f"https://api.lever.co/v0/postings/{company}?mode=json"
    try:
        data = fetch_json(api, session).json()
    except Exception as e:
        # fallback to legacy JSON if needed
        try:
            alt = f"https://jobs.lever.co/{company}.json"
            data = fetch_json(alt, session).json()
        except Exception as e2:
            print(f"[Lever API ERROR] {company}: {e} / {e2}")
            return []

    out = []
    for p in data:
        title = p.get("text") or p.get("title") or ""
        url = p.get("hostedUrl") or p.get("applyUrl") or p.get("url") or ""
        loc = None
        if "categories" in p and isinstance(p["categories"], dict):
            loc = p["categories"].get("location")
        date = p.get("createdAt") or p.get("created_at")
        out.append({
            "title": title,
            "location": loc,
            "date": date,
            "url": url,
            "source": "lever",
            "company": company.title(),
        })
    return out

# ---------------- Generic HTML fallback ----------------

def extract_generic_html(url: str, html: str, company: Optional[str] = None):
    soup = BeautifulSoup(html, "lxml")
    out = []
    for a in soup.select("a[href]"):
        href = a.get("href") or ""
        text = a.get_text(strip=True) or ""
        if "/job" in href.lower() or "/careers/" in href.lower() or "/jobs/" in href.lower():
            out.append({
                "title": text or "Job",
                "url": urllib.parse.urljoin(url, href),
                "source": "unknown",
                "company": (company or "").title() or None,
            })
    return out

# ---------------- Main driver ----------------

def process_url(url: str, session: requests.Session):
    results = []
    company = guess_company_from_url(url)

    # Prefer official APIs when recognized
    if is_greenhouse(url) and company:
        return extract_greenhouse_api(company, session)
    if is_lever(url) and company:
        return extract_lever_api(company, session)

    # Otherwise HTML (respect robots)
    if not can_fetch(url):
        print(f"[SKIP robots] {url}")
        return results

    try:
        html = fetch_html(url, session).text
    except Exception as e:
        print(f"[ERROR fetch HTML] {url}: {e}")
        return results

    return extract_generic_html(url, html, company)

def main():
    ap = argparse.ArgumentParser(description="Scrape startup career pages (API-first, respectful).")
    ap.add_argument("--urls", nargs="+", required=True, help="One or more careers page URLs")
    ap.add_argument("--out", default="data/output.json", help="Output JSON path")
    ap.add_argument("--max-per-site", type=int, default=500, help="Safety cap per site")
    args = ap.parse_args()

    session = requests.Session()
    out_records = []
    for url in args.urls:
        items = process_url(url, session)[: args.max-per-site if hasattr(args, 'max-per-site') else args.max_per_site]  # safe attr
        if not items:
            print(f"[NO ITEMS] {url}")
        for r in items:
            tr = transform(r)
            ok, errs = validate_record(tr)
            if ok:
                out_records.append(tr)
            else:
                print(f"[INVALID] {tr.get('title','(no title)')}: {errs}")

    # Write output
    import os
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out_records, f, indent=2)
    print(f"Wrote {len(out_records)} records to {args.out}")

if __name__ == "__main__":
    main()
