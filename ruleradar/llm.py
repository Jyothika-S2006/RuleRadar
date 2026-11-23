import json
import os
import re
from dotenv import load_dotenv

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")

if GEMINI_KEY:
    from google import genai
    from google.genai import types

    _client = genai.Client(api_key=GEMINI_KEY)
    _model = os.getenv("RR_MODEL", "gemini-3.8-flash")

    def ask_json(system: str, user: str) -> dict:
        config = types.GenerateContentConfig(
            system_instruction=system + "\nReply with a single JSON object and nothing else.",
            response_mime_type="application/json",
            temperature=0.1,
        )
        response = _client.models.generate_content(
            model=_model,
            contents=user,
            config=config,
        )
        text = response.text.strip()
        text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.M).strip()
        return json.loads(text)

elif ANTHROPIC_KEY:
    import anthropic

    _client = anthropic.Anthropic()
    _model = os.getenv("RR_MODEL", "claude-sonnet-5-5")

    def ask_json(system: str, user: str) -> dict:
        msg = _client.messages.create(
            model=_model,
            max_tokens=1200,
            system=system + "\nReply with a single JSON object and nothing else.",
            messages=[{"role": "user", "content": user}],
        )
        text = msg.content[0].text.strip()
        text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.M).strip()
        return json.loads(text)
else:
    def ask_json(system: str, user: str) -> dict:
        raise ValueError("No API key found in .env! Add GEMINI_API_KEY or ANTHROPIC_API_KEY.")
