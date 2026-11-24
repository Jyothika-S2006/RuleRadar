import logging

import pytest

from ruleradar.fetcher import fetch_policy


@pytest.mark.parametrize(
    "input_url",
    [
        "  'http://localhost:8765/live.html'  ",
        '"http://localhost:8765/live.html"',
        "localhost:8765/live.html",
    ],
)
def test_fetch_policy_cleans_url(monkeypatch, caplog, input_url):
    requested_urls = []

    class Response:
        headers = {"content-type": "text/html"}
        text = "<p>demo notice</p>"
        content = b""

        def raise_for_status(self):
            pass

    def fake_get(url, **kwargs):
        requested_urls.append(url)
        return Response()

    monkeypatch.setattr("ruleradar.fetcher.httpx.get", fake_get)
    with caplog.at_level(logging.INFO, logger="ruleradar.fetcher"):
        result = fetch_policy(input_url)

    expected_url = "http://localhost:8765/live.html"
    assert requested_urls == [expected_url]
    assert result["url"] == expected_url
    assert repr(input_url) in caplog.text
