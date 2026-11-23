import difflib

from .fetcher import fetch_and_store
from .llm import ask_json
from .store import last_two

SYSTEM = """You compare two versions of an official notice. Ignore cosmetic changes.
Return JSON: {"changes":[{"field":str,"old":str,"new":str,
"importance":"high|medium|low","who_is_affected":str}]}"""


def raw_changes(old: str, new: str) -> list[str]:
    diff = difflib.unified_diff(old.splitlines(), new.splitlines(), lineterm="", n=0)
    return [l for l in diff if not l.startswith(("+++", "---", "@@"))]


def explain_changes(old: str, new: str) -> dict:
    lines = raw_changes(old, new)
    if not lines:
        return {"changed": False, "changes": []}
    result = ask_json(SYSTEM, "DIFF (- old, + new):\n" + "\n".join(lines[:200]))
    return {"changed": True, **result}


def compare_versions(url: str) -> dict:
    fetch_and_store(url)
    rows = last_two(url)
    if len(rows) < 2:
        return {
            "changed": False,
            "note": "Only one snapshot stored. Run again after the page changes.",
            "source_url": url,
        }
    res = explain_changes(rows[1]["text"], rows[0]["text"])
    res["source_url"] = url
    return res