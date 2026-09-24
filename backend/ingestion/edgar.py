"""
SEC EDGAR collection.

Rate-limited with a serialised lock rather than a token bucket: the SEC
publishes a request-per-second ceiling per caller, and a bucket that refills
smoothly still permits a burst at the boundary. The lock is per-process while
the egress address is shared, so it is correct at one instance and one
Terraform line away from being silently wrong.

Illustrative excerpt — signatures and contracts only. Bodies are elided and
the imports do not resolve, so this file does not run.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Filing:
    accession_number: str
    cik: str
    form_type: str
    filed_at: str
    document_url: str


async def search_filings(cik: str, form_type: str, limit: int) -> list[Filing]:
    """List filings for one company. Requires a contact User-Agent."""
    ...


async def fetch_document(filing: Filing) -> bytes:
    """Download one filing, respecting the serialised request lock."""
    ...
