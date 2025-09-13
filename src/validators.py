from datetime import datetime
from dateutil import parser

REQUIRED_FIELDS = ["title", "url"]

def is_nonempty(s: str) -> bool:
    return isinstance(s, str) and s.strip() != ""

def validate_record(record: dict) -> tuple[bool, list[str]]:
    """Return (ok, errors)."""
    errors: list[str] = []

    for f in REQUIRED_FIELDS:
        if f not in record or not is_nonempty(str(record.get(f, ""))):
            errors.append(f"Missing required field: {f}")

    # Optional: validate date format if present
    if (d := record.get("date")):
        try:
            parser.parse(str(d))
        except Exception:
            errors.append(f"Invalid date: {d!r}")

    # Optional: basic URL sanity
    if (u := record.get("url")) and not str(u).startswith(("http://", "https://")):
        errors.append(f"URL must start with http(s): {u!r}")

    return (len(errors) == 0, errors)
