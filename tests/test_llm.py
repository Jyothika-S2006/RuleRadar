import importlib
from types import SimpleNamespace

import groq


def test_groq_ask_json_sends_json_request(monkeypatch):
    requests = []

    class FakeGroq:
        def __init__(self, api_key):
            assert api_key == "test-key"
            self.chat = SimpleNamespace(
                completions=SimpleNamespace(create=self.create)
            )

        def create(self, **kwargs):
            requests.append(kwargs)
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        message=SimpleNamespace(content='{"verdict":"supported"}')
                    )
                ]
            )

    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("RR_MODEL", raising=False)
    monkeypatch.setattr(groq, "Groq", FakeGroq)

    import ruleradar.llm as llm
    original_namespace = llm.__dict__.copy()
    try:
        importlib.reload(llm)
        assert llm.ask_json("system prompt", "user prompt") == {
            "verdict": "supported"
        }
    finally:
        llm.__dict__.clear()
        llm.__dict__.update(original_namespace)

    request = requests[0]
    assert request["model"] == "openai/gpt-oss-120b"
    assert request["response_format"] == {"type": "json_object"}
    assert request["messages"][1] == {"role": "user", "content": "user prompt"}
