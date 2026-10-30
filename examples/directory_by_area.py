"""One category across the quartieri of a city, from the Pagine Gialle listings.

    python directory_by_area.py idraulico --areas "Milano Quartiere Affori" "Milano Quartiere Niguarda" "Milano Quartiere Isola"

Reads the directory listings for each area (a quartiere, or a comune) from
Pagine Gialle, and from Pagine Bianche too with --sources paginegialle
paginebianche. It keeps only businesses that publish a phone (the others are
not billed), removes the ones already found in an earlier area by the
directory's own id and writes directory.csv with the area that found each
business.
"""

import argparse

from quanticdata_pagine_gialle_scraper import PagineGialleScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("category", help='as the directory names it, e.g. "idraulico"')
    parser.add_argument("--areas", nargs="+", required=True, help='comuni or quartieri, e.g. "Milano Quartiere Affori"')
    parser.add_argument("--sources", nargs="+", default=["paginegialle"],
                        choices=["paginegialle", "paginebianche"])
    parser.add_argument("--per-area", type=int, default=100, help="businesses per area (max 100)")
    parser.add_argument("--out", default="directory.csv")
    args = parser.parse_args()

    pg = PagineGialleScraper()
    found = {}
    for area in args.areas:
        run = pg.directory(args.category, location=area, sources=args.sources, only_with_phone=True,
                           max_results=args.per_area)
        new = 0
        for b in run:
            key = (b["source"], b.get("source_id") or b.get("profile_url") or b["name"])
            if key not in found:
                found[key] = {"area": area, **b}
                new += 1
        print(f"{area}: {len(run)} businesses, {new} not seen in an earlier area")

    rows = list(found.values())
    write(rows, args.out)
    print(f"{len(rows)} businesses written to {args.out}")


if __name__ == "__main__":
    main()
