from .fetcher import fetch_and_store
from .differ import compare_versions
from .llm import ask_json

SYSTEM = """You help a student act on an official notice. Use ONLY facts in the notice.
If unsure, say so. Return JSON:
{"affected":true,"why":str,"checklist":[{"step":str,"deadline":str|null}]}"""

def generate_checklist(url: str, profile: str) -> dict:
    changes = compare_versions(url)
    doc = fetch_and_store(url)
    res = ask_json(
        SYSTEM,
        f"STUDENT PROFILE: {profile}\nCHANGES: {changes}\nNOTICE:\n{doc['text'][:12000]}"
    )
    res["source_url"] = url
    return res
