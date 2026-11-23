import datetime
import logging
import sys

from mcp.server.fastmcp import FastMCP


logging.basicConfig(stream=sys.stderr, level=logging.INFO)
mcp = FastMCP("ruleradar")


def _checked_at() -> str:
    return datetime.datetime.now().isoformat(timespec="seconds")


@mcp.tool()
def fetch_policy(url: str) -> dict:
    """Fetch an allowlisted official page and store a snapshot."""
    try:
        from .fetcher import fetch_and_store
    except ImportError as exc:
        raise RuntimeError("Feature 1 snapshot module is not implemented yet") from exc

    doc = fetch_and_store(url)
    return {
        "source_url": url,
        "sha256": doc["sha256"],
        "preview": doc["text"][:500],
        "checked_at": _checked_at(),
    }


@mcp.tool()
def compare_versions(url: str) -> dict:
    """Compare the latest snapshot with the previous snapshot."""
    try:
        from .differ import compare_versions as compare
    except ImportError as exc:
        raise RuntimeError("Feature 1 snapshot module is not implemented yet") from exc
    return compare(url)


@mcp.tool()
def verify_claim(claim: str, url: str) -> dict:
    """Verify a claim against an allowlisted source."""
    try:
        from .verifier import verify_claim as verify
    except ImportError as exc:
        raise RuntimeError("Feature 2 claim verifier module is not implemented yet") from exc
    return verify(claim, url)


@mcp.tool()
def generate_checklist(url: str, profile: str) -> dict:
    """Create an action checklist for a student profile."""
    try:
        from .checklist import generate_checklist as checklist
    except ImportError as exc:
        raise RuntimeError("Feature 3 checklist module is not implemented yet") from exc
    return checklist(url, profile)


if __name__ == "__main__":
    mcp.run()
