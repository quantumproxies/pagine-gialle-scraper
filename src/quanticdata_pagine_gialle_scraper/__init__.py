"""Pagine Gialle Scraper: Pagine Gialle scraper for Python and the command line: Italian businesses for a category and a comune, with the email the owner registered, Partita IVA, verified phone, website, opening hours and address, plus Pagine Bianche listings, as JSON or CSV. Free and open source; sign in with your QuanticData account, no proxies or headless browser to run.

    from quanticdata_pagine_gialle_scraper import PagineGialleScraper

    scraper = PagineGialleScraper()   # saved login (`pagine-gialle-scraper login`) or QUANTICDATA_API_KEY
    run = scraper.profiles(...)   # Pagine Gialle profiles for a category in a comune, with email and VAT id
    run = scraper.directory(...)   # Pagine Gialle and Pagine Bianche listings for a category in a comune
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["PagineGialleScraper", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class PagineGialleScraper:
    """Pagine Gialle Scraper on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="pagine-gialle-scraper/0.1.0 (+https://github.com/quantumproxies/pagine-gialle-scraper)", timeout=timeout)

    def profiles(
        self, query: str,
        *,
        location: str,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Italian businesses for a category and a comune, read from their Pagine Gialle profile: the email the owner registered, VAT id, verified phone, opening hours.

        Args:
            query: What the businesses do, as Pagine Gialle names it — e.g. "dentisti", "idraulico", "ristoranti".
            location: Italian comune, e.g. "Torino", "Monza".
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            max_results: How many profiles to deliver at most (1–300). You pay only for delivered profiles.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 300 rows, one per profile: see ``types.PaginegialleProfilesRow``.
        """
        payload = {
            "query": query,
            "location": location,
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("paginegialle_profiles", payload, wait=wait, timeout=timeout)

    def directory(
        self, query: str,
        *,
        location: str,
        sources: Optional[Union[str, Sequence[str]]] = None,
        only_with_phone: Optional[bool] = None,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Businesses listed in Italian directories (Pagine Gialle, Pagine Bianche) for a category and a comune or quartiere, including the small ones Google misses.

        Args:
            query: What the businesses do, as the directory categorises it — e.g. "autonoleggio", "dentista", "idraulico".
            location: Comune or quartiere — e.g. "Milano", "Milano Quartiere Affori", "Monza".
            sources: Directories to read: paginegialle (default), paginebianche, or both, e.g. --sources paginegialle paginebianche. One of: paginegialle, paginebianche.
            only_with_phone: Drop and do not bill businesses with no published phone number.
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            max_results: How many businesses to deliver at most (1–100). You pay only for delivered businesses.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 100 rows, one per business: see ``types.BusinessDirectoryRow``.
        """
        payload = {
            "query": query,
            "location": location,
            "sources": _as_list(sources),
            "only_with_phone": only_with_phone,
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("business_directory", payload, wait=wait, timeout=timeout)
