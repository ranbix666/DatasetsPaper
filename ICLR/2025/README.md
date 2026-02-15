# ICLR 2025 OpenReview data

- **Source**: OpenReview API v2 (`api2.openreview.net`), venue `ICLR.cc/2025/Conference`.
- **Schema**: Same as ICLR 2024 — one row per official review, with full discussion thread (rebuttals, meta-reviews).

## Output

- `iclr2025_full_transcript.csv`: columns `paper_number`, `paper_title`, `decision`, `review_id`, `rating`, `confidence`, `review_text`, `discussion_transcript`.

## How to collect

1. Install: `pip install openreview-py "urllib3<2.0" tqdm`
2. Open `collect_iclr2025.ipynb` and run all cells.

**Rate limiting**: OpenReview allows 60 requests/minute. The notebook throttles requests (~1.05 s between each forum fetch) and retries on 429 with a 65 s backoff. With ~11.6k submissions, a full run takes about **3–4 hours**.
