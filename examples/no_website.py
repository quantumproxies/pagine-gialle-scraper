"""Businesses of a category in a comune that link no website, from Pagine Gialle.

    python no_website.py ristoranti --location Bergamo --max 200

Reads the Pagine Gialle profiles and keeps the ones whose profile links no
website (social pages do not count as one). Writes no_website.csv with name,
phone, email, address and the social pages they do have.
"""

import argparse

from quanticdata_pagine_gialle_scraper import PagineGialleScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("category", help='as Pagine Gialle names it, e.g. "ristoranti"')
    parser.add_argument("--location", required=True, help="Italian comune")
    parser.add_argument("--max", type=int, default=200, help="profiles to read (max 300)")
    parser.add_argument("--out", default="no_website.csv")
    args = parser.parse_args()

    pg = PagineGialleScraper()
    run = pg.profiles(args.category, location=args.location, max_results=args.max)
    rows = []
    for b in run:
        if b.get("website"):
            continue
        socials = {k: v for k, v in (b.get("socials") or {}).items() if v}
        rows.append({"name": b["name"], "phone": b.get("phone"), "email": b.get("email"),
                     "street": b.get("street"), "postal_code": b.get("postal_code"), "city": b.get("city"),
                     "province": b.get("province"), "rating": b.get("rating"), "reviews": b.get("reviews"),
                     "social_pages": sorted(socials.values()), "profile_url": b["profile_url"]})

    write(rows, args.out)
    print(f"{len(rows)} of {len(run)} businesses link no website, written to {args.out}")


if __name__ == "__main__":
    main()
