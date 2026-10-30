# Pagine Gialle Scraper

[![ci](https://github.com/quantumproxies/pagine-gialle-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/pagine-gialle-scraper/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Scrape Pagine Gialle, the Italian business directory, from Python or the command line: the businesses listed for a category in a comune, with the contact email the owner registered, the Partita IVA and codice fiscale, the verified phone, website, opening hours, services and address, as JSON or CSV. A second command reads the listing pages of Pagine Gialle and Pagine Bianche, small businesses included. The code is free and open source (MIT). It runs on the QuanticData Data API, so there are no proxies to rotate and no headless browser to keep alive: sign in once and run a command.

```bash
pip install git+https://github.com/quantumproxies/pagine-gialle-scraper
pagine-gialle-scraper login
pagine-gialle-scraper profiles dentisti --location Torino --max-results 60 -o dentisti_torino.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=pagine-gialle-scraper).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `pagine-gialle-scraper profiles` | category (in Italian), comune | Name, email, Partita IVA, verified phone, website, opening hours, 26 fields per row | up to 300 |
| `pagine-gialle-scraper directory` | category (in Italian), comune or quartiere | Name, category, address, phones, website, opening hours, 20 fields per row ([fields and price](https://quanticdata.io/collectors/business-directory-api/?utm_source=github&utm_medium=readme&utm_campaign=pagine-gialle-scraper)) | up to 100 |

Both commands cover Italy and take Italian input: a category as the directory names it ("dentisti", "idraulico", "autonoleggio") and a comune ("Torino", "Milano"); `directory` also takes a quartiere ("Milano Quartiere Affori"). `profiles` opens each business profile for the email, Partita IVA, codice fiscale, legal name, social pages and payment methods; `directory` is the lighter read of the listing pages, with `--only-with-phone` to drop and not bill the businesses that publish no number.

## Sample output

A real row from `pagine-gialle-scraper profiles dentisti --location Torino --max-results 3` (2026-10-23):

```json
{
  "city": "Torino",
  "name": "Studio Medico Odontoiatrico Bosco",
  "rank": 2,
  "email": "studiogbosco@gmail.com",
  "phone": "+39 011 655355",
  "rating": 5,
  "region": "Piemonte",
  "street": "Via Madama Cristina, 6",
  "tax_id": null,
  "vat_id": "11247730010",
  "reviews": 1,
  "socials": {},
  "website": "https://www.studiogbosco.it",
  "category": "Dentist",
  "latitude": 45.05985,
  "province": "TO",
  "services": null,
  "longitude": 7.68439,
  "sponsored": true,
  "legal_name": "STUDIO DI ODONTOIATRIA BOSCO",
  "description": "Lo Studio Odontoiatrico Bosco è un centro di eccellenza specializzato in chirurgia maxillo-facciale e nella cura di patologie dell'articolazione temporo-mandibolare (A.T.M.).",
  "postal_code": "10125",
  "profile_url": "https://www.paginegialle.it/studiodentisticobosco",
  "opening_hours": [
    "Mo 14:30 - 20:00",
    "Tu 14:30 - 20:00",
    "We 14:30 - 20:00",
    "Th 14:30 - 20:00",
    "Fr 14:30 - 17:00"
  ],
  "payment_methods": null,
  "listing_category": "dentisti"
}
```

## Python

```python
from quanticdata_pagine_gialle_scraper import PagineGialleScraper

pg = PagineGialleScraper()  # saved login, or QUANTICDATA_API_KEY

dentisti = pg.profiles("dentisti", location="Torino", max_results=60)
for b in dentisti:
    print(b["name"], b["email"], b["vat_id"], b["phone"], b["city"])
dentisti.to_csv("dentisti_torino.csv")

noleggi = pg.directory("autonoleggio", location="Milano", only_with_phone=True, max_results=100)
print(len(noleggi), "businesses;", sum(1 for b in noleggi if not b["website"]), "without a website")
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Leads with email and VAT id**: Run a few categories in a few comuni, keep the businesses that publish an email, deduplicate them by Partita IVA and get one CSV ready for a CRM. See [`examples/leads_with_email.py`](examples/leads_with_email.py).
- **Businesses without a website**: List the businesses of a category in a comune that link no website from their profile, with phone, email and address: a prospect list for web agencies. See [`examples/no_website.py`](examples/no_website.py).
- **A whole city, quartiere by quartiere**: Read the directory listings for each quartiere of a city, from Pagine Gialle and optionally Pagine Bianche, keep the businesses with a phone and deduplicate them by the directory's own id. See [`examples/directory_by_area.py`](examples/directory_by_area.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `pagine-gialle-scraper run <id> -o out.csv` collects it later.

### `pagine-gialle-scraper profiles`

Italian businesses for a category and a comune, read from their Pagine Gialle profile: the email the owner registered, VAT id, verified phone, opening hours.

```
pagine-gialle-scraper profiles QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | What the businesses do, as Pagine Gialle names it — e.g. "dentisti", "idraulico", "ristoranti". |
| `--location` | string |  | Italian comune, e.g. "Torino", "Monza". Required. |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--max-results` | integer | `25` | How many profiles to deliver at most (1–300). You pay only for delivered profiles. |

### `pagine-gialle-scraper directory`

Businesses listed in Italian directories (Pagine Gialle, Pagine Bianche) for a category and a comune or quartiere, including the small ones Google misses.

```
pagine-gialle-scraper directory QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | What the businesses do, as the directory categorises it — e.g. "autonoleggio", "dentista", "idraulico". |
| `--location` | string |  | Comune or quartiere — e.g. "Milano", "Milano Quartiere Affori", "Monza". Required. |
| `--sources` | paginegialle / paginebianche |  | Directories to read: paginegialle (default), paginebianche, or both, e.g. --sources paginegialle paginebianche. |
| `--only-with-phone` | boolean | `False` | Drop and do not bill businesses with no published phone number. |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--max-results` | integer | `25` | How many businesses to deliver at most (1–100). You pay only for delivered businesses. |

## Output fields

<details><summary><code>pagine-gialle-scraper profiles</code>: 26 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position, listing order first, then category pages. |
| `name` | string | Business name as registered. |
| `category` | string or null | Category or schema type of the profile. |
| `email` | string or null | Contact email the owner registered on the profile. Null when none is published. |
| `phone` | string or null | The phone number the directory marks as verified. |
| `website` | string or null | Website linked from the profile, when one is (social pages excluded). |
| `vat_id` | string or null | Partita IVA. |
| `tax_id` | string or null | Codice fiscale. |
| `street` | string or null | Street and number. |
| `postal_code` | string or null | CAP. |
| `city` | string or null | Comune. |
| `region` | string or null | Region. |
| `latitude` | number or null | Latitude. |
| `longitude` | number or null | Longitude. |
| `opening_hours` | string[] or null | Opening hours as published, e.g. "Mo 10:00 - 19:00". |
| `services` | string[] or null | Services the owner listed. |
| `description` | string or null | Profile description, as plain text. |
| `profile_url` | string | The profile page — the de-duplication key. |
| `legal_name` | string or null | Registered name of the business. |
| `province` | string or null | Two-letter province code. |
| `rating` | number or null | User rating on the directory (1–5). |
| `reviews` | integer or null | Review count on the directory. |
| `payment_methods` | string[] or null | Payment methods the business accepts. |
| `socials` | object | { facebook, instagram, linkedin, youtube, tiktok, twitter } pages linked from the profile. |
| `listing_category` | string or null | The directory's own category label for the business (Italian), when it came from the search listing. |
| `sponsored` | boolean | True for the placements the directory marks as suggested in the search listing. |

</details>

<details><summary><code>pagine-gialle-scraper directory</code>: 20 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position in the merged result set. |
| `name` | string | Business name as listed. |
| `category` | string or null | The directory's own category for the business. |
| `address` | string or null | Full printed address. |
| `street` | string or null | Street and number. |
| `postal_code` | string or null | CAP. |
| `city` | string or null | Comune. |
| `province` | string or null | Two-letter province code. |
| `phone` | string or null | First published phone number. |
| `phones` | string[] | Every phone number on the listing. |
| `description` | string or null | Blurb the business published on the listing, when it has one. |
| `profile_url` | string or null | The directory page for this business. |
| `source` | string | Which directory delivered the row. |
| `source_id` | string or null | The directory's own id — a stable dedup key. |
| `website` | string or null | The business's own website, when the listing links one. |
| `whatsapp` | string or null | WhatsApp contact as https://wa.me/&lt;number&gt;, when the listing has the button. |
| `reviews` | integer or null | Review count shown next to the stars. |
| `opening_hours` | string[] or null | Weekly hours from the listing, one entry per opening range: "Mo 09:00 - 13:00", "Mo 14:00 - 19:00". |
| `sponsored` | boolean | True for the placements the directory marks as suggested. |
| `listing_type` | string or null | "paid", "free" or "self" — the kind of listing the business holds on the directory. |

</details>

## Sign-in and API keys

- `pagine-gialle-scraper login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `pagine-gialle-scraper login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `pagine-gialle-scraper login --api-key`.
- `pagine-gialle-scraper logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the prices listed in the [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=pagine-gialle-scraper); $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=pagine-gialle-scraper).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/paginegialle_profiles/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"query": "dentisti", "location": "Torino", "max_results": 3}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=pagine-gialle-scraper) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=pagine-gialle-scraper) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this Pagine Gialle scraper free?**

The code is free and MIT-licensed. Scraping runs on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the prices listed in the API reference. Failed runs are never billed.

**Do I need proxies or a headless browser?**

No. You send a category and a comune and get rows back; the requests run on QuanticData's side.

**How many businesses can one run return?**

Up to 300 businesses per run with profiles and up to 100 with directory; ask for fewer with --max-results and you pay only for what is delivered.

**Can I export to CSV or Excel?**

Add -o results.csv (or .json, .jsonl). Lists such as opening hours and services are joined with '; ' and social pages become socials.facebook, socials.instagram and so on, so the CSV opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/leads_with_email.py from cron, GitHub Actions or any scheduler.

**Can I use the emails for marketing?**

It reads public business profiles only: the email is the one the business registered on its own profile. You are responsible for the directory's terms and for the data-protection and direct-marketing rules (GDPR, the Italian privacy code) that apply to how you use the data.

## Related scrapers

- [Google Maps Scraper](https://github.com/quantumproxies/google-maps-scraper): Google Maps scraper for Python and the command line.
- [MioDottore Scraper API](https://github.com/quantumproxies/miodottore-scraper): MioDottore scraper for Python and the command line.
- [Email Extractor](https://github.com/quantumproxies/email-extractor): Email extractor for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=pagine-gialle-scraper).
