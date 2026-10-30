"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class PaginegialleProfilesRow(TypedDict, total=False):
    """One row of `pagine-gialle-scraper profiles` (paginegialle_profiles v1.1.2)."""

    rank: int
    """1-based position, listing order first, then category pages."""
    name: str
    """Business name as registered."""
    category: Optional[str]
    """Category or schema type of the profile."""
    email: Optional[str]
    """Contact email the owner registered on the profile. Null when none is published."""
    phone: Optional[str]
    """The phone number the directory marks as verified."""
    website: Optional[str]
    """Website linked from the profile, when one is (social pages excluded)."""
    vat_id: Optional[str]
    """Partita IVA."""
    tax_id: Optional[str]
    """Codice fiscale."""
    street: Optional[str]
    """Street and number."""
    postal_code: Optional[str]
    """CAP."""
    city: Optional[str]
    """Comune."""
    region: Optional[str]
    """Region."""
    latitude: Optional[float]
    """Latitude."""
    longitude: Optional[float]
    """Longitude."""
    opening_hours: Optional[List[str]]
    """Opening hours as published, e.g. "Mo 10:00 - 19:00"."""
    services: Optional[List[str]]
    """Services the owner listed."""
    description: Optional[str]
    """Profile description, as plain text."""
    profile_url: str
    """The profile page — the de-duplication key."""
    legal_name: Optional[str]
    """Registered name of the business."""
    province: Optional[str]
    """Two-letter province code."""
    rating: Optional[float]
    """User rating on the directory (1–5)."""
    reviews: Optional[int]
    """Review count on the directory."""
    payment_methods: Optional[List[str]]
    """Payment methods the business accepts."""
    socials: Dict[str, Any]
    """{ facebook, instagram, linkedin, youtube, tiktok, twitter } pages linked from the profile."""
    listing_category: Optional[str]
    """The directory's own category label for the business (Italian), when it came from the search listing."""
    sponsored: bool
    """True for the placements the directory marks as suggested in the search listing."""

class BusinessDirectoryRow(TypedDict, total=False):
    """One row of `pagine-gialle-scraper directory` (business_directory v1.1.1)."""

    rank: int
    """1-based position in the merged result set."""
    name: str
    """Business name as listed."""
    category: Optional[str]
    """The directory's own category for the business."""
    address: Optional[str]
    """Full printed address."""
    street: Optional[str]
    """Street and number."""
    postal_code: Optional[str]
    """CAP."""
    city: Optional[str]
    """Comune."""
    province: Optional[str]
    """Two-letter province code."""
    phone: Optional[str]
    """First published phone number."""
    phones: List[str]
    """Every phone number on the listing."""
    description: Optional[str]
    """Blurb the business published on the listing, when it has one."""
    profile_url: Optional[str]
    """The directory page for this business."""
    source: str
    """Which directory delivered the row."""
    source_id: Optional[str]
    """The directory's own id — a stable dedup key."""
    website: Optional[str]
    """The business's own website, when the listing links one."""
    whatsapp: Optional[str]
    """WhatsApp contact as https://wa.me/<number>, when the listing has the button."""
    reviews: Optional[int]
    """Review count shown next to the stars."""
    opening_hours: Optional[List[str]]
    """Weekly hours from the listing, one entry per opening range: "Mo 09:00 - 13:00", "Mo 14:00 - 19:00"."""
    sponsored: bool
    """True for the placements the directory marks as suggested."""
    listing_type: Optional[str]
    """"paid", "free" or "self" — the kind of listing the business holds on the directory."""
