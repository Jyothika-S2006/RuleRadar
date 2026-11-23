import datetime
from .fetcher import fetch_and_store
from .store import last_two
from .llm import ask_json

SYSTEM = """Decide whether the SOURCE supports the CLAIM. Return JSON:
{"verdict":"supported|contradicted|not_found",
 "quote":"one sentence copied EXACTLY from SOURCE, or empty","reason":str}"""

def _check(claim: str, text: str) -> dict:
    res = ask_json(SYSTEM, f"CLAIM: {claim}\n\nSOURCE:\n{text[:15000]}")
    quote = res.get("quote") or ""
    if quote and quote not in text:
        res.update(
            verdict="unverified",
            quote="",
            reason="Quote not found verbatim in source; discarded."
        )
    return res

def verify_claim(claim: str, url: str) -> dict:
    doc = fetch_and_store(url)
    res = _check(claim, doc["text"])
    if res["verdict"] != "supported":
        rows = last_two(url)
        if len(rows) == 2 and _check(claim, rows[1]["text"])["verdict"] == "supported":
            res["verdict"] = "outdated"
            res["reason"] = "Claim matched an older version of this page, not the current one."
    res["source_url"] = url
    res["checked_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    return res
