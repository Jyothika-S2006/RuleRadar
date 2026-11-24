# RuleRadar

RuleRadar is an MCP server for tracking official scholarship, exam, and recruitment notices.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Add a `GROQ_API_KEY`, `GEMINI_API_KEY`, or `ANTHROPIC_API_KEY` to `.env` for the LLM features. When using Groq, the default model is `openai/gpt-oss-120b`; set `RR_MODEL` to override it.

## MCP tools

- `fetch_policy`: fetch an allowlisted page and store a snapshot
- `compare_versions`: compare two snapshots and describe meaningful changes
- `verify_claim`: verify a claim and return evidence or an honest failure
- `generate_checklist`: turn notice facts and a student profile into action steps

## Run

```powershell
npx @modelcontextprotocol/inspector python -m ruleradar.server
```

The demo notice pages and feature modules are owned by the team feature branches.
