import hashlib
import io
import re
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup
from pypdf import PdfReader

from . import store

# Only the official sites you will demo. localhost is for the demo page.
ALLOWED_DOMAINS = {"localhost", "127.0.0.1", "vtu.ac.in", "scholarships.gov.in"}


def is_allowed(url: str) -> bool:
    host = urlparse(url).hostname or ""
    return any(host == d or host.endswith("." + d) for d in ALLOWED_DOMAINS)


def clean_text(html: str) -> str:
    """Strip scripts/menus and collapse whitespace so cosmetic changes do not count."""
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "nav", "footer", "noscript"]):
        tag.decompose()
    lines = (re.sub(r"\s+", " ", l).strip() for l in soup.get_text("\n").splitlines())
    return "\n".join(l for l in lines if l)


def _extract_pdf_text(content: bytes) -> str:
    reader = PdfReader(io.BytesIO(content))
    pages = [page.extract_text() or "" for page in reader.pages]
    lines = (re.sub(r"\s+", " ", l).strip() for l in "\n".join(pages).splitlines())
    return "\n".join(l for l in lines if l)


def fetch_policy(url: str) -> dict:
    if not is_allowed(url):
        raise ValueError(f"Domain not allowlisted: {url}")
    try:
        r = httpx.get(
            url,
            timeout=20,
            follow_redirects=True,
            headers={"User-Agent": "RuleRadar/0.1 (student project)"},
        )
        r.raise_for_status()
    except httpx.TimeoutException as exc:
        raise RuntimeError(f"Request timed out while fetching {url}") from exc
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"HTTP {exc.response.status_code} error while fetching {url}"
        ) from exc

    content_type = r.headers.get("content-type", "").lower()
    if "application/pdf" in content_type or urlparse(url).path.lower().endswith(".pdf"):
        text = _extract_pdf_text(r.content)
    else:
        text = clean_text(r.text)

    return {
        "url": url,
        "text": text,
        "sha256": hashlib.sha256(text.encode()).hexdigest(),
    }


def fetch_and_store(url: str) -> dict:
    """Fetch, and save a new snapshot only if the content changed."""
    doc = fetch_policy(url)
    rows = store.last_two(url)
    if not rows or rows[0]["sha256"] != doc["sha256"]:
        store.save_snapshot(url, doc["text"], doc["sha256"])
    return doc