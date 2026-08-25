# Business directory API — examples

Businesses listed in Italian directories for a category and a place — the small ones Google misses.

**Live page, full schema & pricing → [quanticdata.io/collectors/business-directory-api/](https://quanticdata.io/collectors/business-directory-api/)**

Reads the listing a business directory publishes for a category in a place and delivers one row per business: name, category, the printed address split into street, postal code, city and province, phone numbers, the directory profile URL and its own id. This is the channel that reaches operators with no web presence — they appear because they are listed, not because they rank. Measured on 'autonoleggio' in Milano, a web search returned ten national chains and no independents, while the directory returned mostly independents. One fetch per source, ~25 businesses; widen coverage by asking for more comuni or quartieri rather than by paging, which these sites serve over XHR.

## Quick start (curl)

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/business_directory/run \
  -H "Authorization: Bearer $QD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "autonoleggio", "location": "Milano", "max_results": 25}'
```

## Python

See [`example.py`](example.py):

```bash
export QD_API_KEY=qd_live_...   # https://quanticdata.io/
python3 example.py
```

## Inputs

- `query` (string, required) — What the businesses do, as the directory categorises it — e.g. "autonoleggio", "dentista", "idraulico".
- `location` (string, required) — Comune or quartiere — e.g. "Milano", "Milano Quartiere Affori", "Monza".
- `sources` (array) — Which directories to read (default paginegialle). Pagine Bianche is best-effort: it refuses repeated requests more often.
- `only_with_phone` (boolean) — Drop and do not bill businesses with no published phone number.
- `country` (string) — ISO 3166-1 alpha-2 code — proxy exit geo and Google locale (gl). Omit for the default pool.
- `max_results` (integer) — How many businesses to deliver at most (1–100). You pay only for delivered businesses.

## Output — one row per business

| field | type | description |
|---|---|---|
| `rank` | integer | 1-based position in the merged result set. |
| `name` | string | Business name as listed. |
| `category` | string | The directory's own category for the business. |
| `address` | string | Full printed address. |
| `street` | string | Street and number. |
| `postal_code` | string | CAP. |
| `city` | string | Comune. |
| `province` | string | Two-letter province code. |
| `phone` | string | First published phone number. |
| `phones` | string[] | Every phone number on the listing. |
| `description` | string | Blurb the business published on the listing, when it has one. |
| `profile_url` | string | The directory page for this business. |
…and 2 more fields — full schema on the [live page](https://quanticdata.io/collectors/business-directory-api/).

## Pricing

**$0.001 per delivered business** ($1.0 per 1,000). A run that delivers nothing costs nothing, and failed rows are never billed. The $2/month free allowance covers roughly 2,000 businesss — no card required.

## Links

- This collector: https://quanticdata.io/collectors/business-directory-api/
- All collectors: https://quanticdata.io/collectors/
- Docs: https://quanticdata.io/docs/
