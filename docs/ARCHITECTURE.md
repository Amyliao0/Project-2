# ARCHITECTURE.md

## Overview
- **Fetcher** (requests + exponential backoff + retry)
- **Extractor** (ATS-specific parsers: Greenhouse, Lever, etc.)
- **Validation** (schema checks via `validators.py`)
- **Transform** (normalize to canonical schema in `transformers.py`)
- **Output** (JSON in `data/output.json`)

## Failure Design
- Exponential backoff with jitter
- Max retries per URL
- Per-domain pacing (sleep windows)
- Skip & log pages that fail validation/extraction

## Extensibility
- Add new `extract_*` functions for other ATSs.
- Add enrichers (e.g., infer department from title keywords).

## CLI
`scraper.py --urls URL1 URL2 ... --out data/output.json --max-per-site 200`
