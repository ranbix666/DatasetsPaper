# ICLR OpenReview Data Collection

## Why 2013–2017 Return Empty

The OpenReview API **does not expose submission data for ICLR 2013–2017**. Both `Blind_Submission` and `Submission` invitations return 0 notes for these years. Data is only available via the API starting from **ICLR 2018**.

- **Blind_Submission**: Returns only *active* submissions (currently under review). Past conferences have none.
- **Submission**: Returns all submissions regardless of status. The invitation does not exist (404) for 2013–2017 in the API.

This appears to be a limitation of how older ICLR venues were migrated to the current OpenReview API.

## Workaround for 2017

The 2017 notebook includes a fallback: when the API returns 0, it fetches from [ahmaurya/iclr2017-reviews-dataset](https://github.com/ahmaurya/iclr2017-reviews-dataset) (pre-crawled papers CSV).

## Alternatives for 2013–2016

For 2013–2016, no equivalent pre-crawled datasets were found in common repos. Options:

1. **Web scraping**: Scrape the OpenReview submission pages (e.g. `https://openreview.net/submissions?venue=ICLR.cc/2016/conference`).
2. **Manual export**: If OpenReview provides export tools for those venues, use them.
3. **Contact OpenReview**: Request API access for historical ICLR data.

## API Coverage

| Year | API (Blind_Submission) | Notes |
|------|------------------------|-------|
| 2013–2017 | 0 | No data in API |
| 2018 | ✓ 935 | |
| 2019 | ✓ 1,419 | |
| 2020 | ✓ 2,213 | |
| 2021+ | ✓ | |
