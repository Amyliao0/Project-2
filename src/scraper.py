#!/usr/bin/env python3
import argparse, csv, json, random, time, urllib.parse
from typing import Optional

import requests
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

from validators import validate_record
from transformers import transform

# ---------------- Catalog helpers ----------------

def load_catalog(path: str):
    """Load startup catalog CSV into a list of dicts."""
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append({
                "name": (r.get("name") or "").strip(),
                "industry": (r.get("industry") or "").strip().lower(),
                "url": (r.get("url") or "").strip(),
            })
    return rows

def urls_for_industry(rows, industry: str):
    """Return URLs for a given industry label (case-insensitive)."""
    wanted = industry.strip().lower()
    return [r["url"] for r in rows if r.get("industry") == wanted and r.get("url")]

# ---------------- Globals ----------------

API_UA = "StartupHiringRadar/0.1 (+contact: your-email@example.com)"

@retry(wait=wait_exponential_jitter(exp_base=2, max=10), stop=stop_after_attempt(3))
def fetch_json(url: str, session: Optional[requests.Session] = None) -> requests.Response:
    sess = session or requests.Session()
    headers = {"User-Agent": API_UA, "Accept": "application/json"}
    resp = sess.get(url, headers=headers, timeout=20)
    resp.raise_for_status()
    time.sleep(0.5 + random.random())
    return resp

# ---------------- Greenhouse helpers ----------------

def is_greenhouse_board(url: str) -> bool:
    return urllib.parse.urlparse(url).netloc == "boards.greenhouse.io"

def greenhouse_slug_from_url(url: str) -> Optional[str]:
    """
    Expects: https://boards.greenhouse.io/<slug>[/*]
    Returns None if not a Greenhouse board URL.
    """
    if not is_greenhouse_board(url):
        return None
    path = urllib.parse.urlparse(url).path.strip("/")
    if not path:
        return None
    # slug is the first segment after domain
    return path.split("/")[0].lower()

def extract_greenhouse_api(company: str, session: Optional[requests.Session] = None):
    """
    Use the official public Greenhouse API:
      https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true
    """
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

# ---------------- Main driver ----------------

def main():
    ap = argparse.ArgumentParser(
        description="Scrape Greenhouse boards (API-first). Use either --urls OR --industry."
    )
    # exactly one of these is required
    mx = ap.add_mutually_exclusive_group(required=True)
    mx.add_argument("--urls", nargs="+", help="One or more Greenhouse board URLs (https://boards.greenhouse.io/<slug>)")
    mx.add_argument("--industry", help="Industry tag to filter startups from --catalog (e.g. ai, fintech)")

    ap.add_argument("--catalog", default="data/startups.csv",
                    help="CSV with columns: name,industry,url (Greenhouse URLs only). Used only with --industry.")
    ap.add_argument("--out", default="data/output.json", help="Output JSON path")
    ap.add_argument("--max-per-site", type=int, default=500, help="Safety cap per site")
    args = ap.parse_args()

    # ——— build targets ———
    target_urls = []
    if args.urls:
        target_urls = args.urls
    else:
        # industry mode
        try:
            rows = load_catalog(args.catalog)
        except FileNotFoundError:
            print(f"[CATALOG] Not found: {args.catalog}")
            return
        target_urls = urls_for_industry(rows, args.industry)
        if not target_urls:
            print(f"No Greenhouse targets found for industry '{args.industry}'. "
                  f"Check {args.catalog} has Greenhouse board URLs for that industry.")
            return

    # de-dupe + keep only boards.greenhouse.io
    seen, urls = set(), []
    for u in target_urls:
        if not u or u in seen:
            continue
        seen.add(u)
        if urllib.parse.urlparse(u).netloc == "boards.greenhouse.io":
            urls.append(u)
        else:
            print(f"[SKIP non-Greenhouse] {u}")

    if not urls:
        print("No Greenhouse targets found. Provide valid boards.greenhouse.io URLs "
              "or ensure your catalog URLs are Greenhouse boards.")
        return

    # ——— scrape ———
    session = requests.Session()
    out_records = []

    for board_url in urls:
        slug = greenhouse_slug_from_url(board_url)
        if not slug:
            print(f"[SKIP invalid Greenhouse URL] {board_url}")
            continue

        items = extract_greenhouse_api(slug, session)
        if not items:
            print(f"[NO ITEMS] {board_url} (check slug/network)")
            continue

        for r in items[: args.max_per_site]:
            tr = transform(r)
            ok, errs = validate_record(tr)
            if ok:
                out_records.append(tr)
            else:
                print(f"[INVALID] {tr.get('title','(no title)')}: {errs}")

    # ——— write ———
    import os
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out_records, f, indent=2)
    print(f"Wrote {len(out_records)} records to {args.out}")


if __name__ == "__main__":
    main()
