This repo is RuleRadar, a Python 3.11 MCP server using the official `mcp` SDK and FastMCP.

- Use type hints and short docstrings. Keep functions small.
- NEVER print() to stdout in server code: stdio MCP breaks. Use logging to stderr.
- Only fetch URLs on the allowlist in `ruleradar/fetcher.py`.
- Any quote returned by the LLM must exist verbatim in the fetched text.
- LLM calls go through `ruleradar.llm.ask_json()` only.
- Return JSON-serialisable dictionaries from tools.
- Every tool result includes `source_url` and a timestamp when applicable.
- Do not add new dependencies without asking.
