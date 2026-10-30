"""Italian businesses that publish an email, for several categories and comuni.

    python leads_with_email.py --categories dentisti idraulico --comuni Torino Monza --per-search 100

Reads the Pagine Gialle profiles, keeps the ones with an email the owner
registered, deduplicates them by Partita IVA (or profile URL when there is
none) and writes leads.csv with the columns a CRM import needs.
"""

import argparse

from quanticdata_pagine_gialle_scraper import PagineGialleScraper, write

FIELDS = ["category_searched", "comune_searched", "name", "legal_name", "email", "phone", "website", "vat_id",
          "street", "postal_code", "city", "province", "region", "listing_category", "profile_url"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--categories", nargs="+", required=True, help='as Pagine Gialle names them, e.g. "dentisti"')
    parser.add_argument("--comuni", nargs="+", required=True, help="Italian comuni, e.g. Torino Monza")
    parser.add_argument("--per-search", type=int, default=100, help="profiles per category and comune (max 300)")
    parser.add_argument("--out", default="leads.csv")
    args = parser.parse_args()

    pg = PagineGialleScraper()
    leads = {}
    for category in args.categories:
        for comune in args.comuni:
            run = pg.profiles(category, location=comune, max_results=args.per_search)
            with_email = [b for b in run if b.get("email")]
            for b in with_email:
                key = b.get("vat_id") or b["profile_url"]
                leads.setdefault(key, {"category_searched": category, "comune_searched": comune, **b})
            print(f"{category} / {comune}: {len(run)} profiles, {len(with_email)} with an email")

    rows = [{k: lead.get(k) for k in FIELDS} for lead in leads.values()]
    write(rows, args.out)
    print(f"{len(rows)} unique businesses written to {args.out}")


if __name__ == "__main__":
    main()
