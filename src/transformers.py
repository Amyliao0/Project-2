import re
from datetime import datetime
from dateutil import parser

CANONICAL_FIELDS = ["title", "department", "location", "date", "url", "source", "company"]

def normalize_date(d: str | None) -> str | None:
    if not d:
        return None
    try:
        dt = parser.parse(d)
        return dt.date().isoformat()
    except Exception:
        return None

def infer_department_from_title(title: str | None) -> str | None:
    if not title:
        return None
    t = title.lower()
    if any(k in t for k in ["engineer", "ml", "data", "ios", "android", "frontend", "backend", "full stack"]):
        return "Engineering"
    if any(k in t for k in ["recruit", "people", "talent", "hr"]):
        return "People/HR"
    if any(k in t for k in ["marketing", "growth", "brand", "content"]):
        return "Marketing"
    if any(k in t for k in ["product manager", "pm", "product"]):
        return "Product"
    return None

def transform(raw: dict) -> dict:
    """Return a new dict in canonical schema; keep unknown fields out."""
    out = {
        "title": (raw.get("title") or "").strip(),
        "department": raw.get("department") or infer_department_from_title(raw.get("title")),
        "location": (raw.get("location") or "").strip() or None,
        "date": normalize_date(raw.get("date")),
        "url": raw.get("url"),
        "source": raw.get("source"),
        "company": raw.get("company"),
    }
    return {k: v for k, v in out.items() if v is not None}
