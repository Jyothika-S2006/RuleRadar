import sqlite3
import time

DB_PATH = "ruleradar.db"


def _conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    c.execute("""CREATE TABLE IF NOT EXISTS snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, fetched_at REAL,
        sha256 TEXT, text TEXT)""")
    return c


def save_snapshot(url: str, text: str, sha256: str) -> None:
    with _conn() as c:
        c.execute(
            "INSERT INTO snapshots (url, fetched_at, sha256, text) VALUES (?,?,?,?)",
            (url, time.time(), sha256, text),
        )


def last_two(url: str):
    """Newest first: [latest, previous]."""
    with _conn() as c:
        return c.execute(
            "SELECT * FROM snapshots WHERE url=? ORDER BY id DESC LIMIT 2",
            (url,),
        ).fetchall()