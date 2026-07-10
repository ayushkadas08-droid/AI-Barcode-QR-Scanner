import sqlite3
from datetime import datetime

from config import DATABASE_PATH


def init_history_db():
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_filename TEXT NOT NULL,
                code_type TEXT NOT NULL,
                decoded_data TEXT NOT NULL,
                category TEXT,
                safety_level TEXT,
                safety_score INTEGER,
                action TEXT,
                ai_summary TEXT,
                created_at TEXT NOT NULL
            )
            """
        )


def save_scan_results(image_filename, results):
    if not results:
        return

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with _connect() as connection:
        connection.executemany(
            """
            INSERT INTO scans (
                image_filename,
                code_type,
                decoded_data,
                category,
                safety_level,
                safety_score,
                action,
                ai_summary,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [_build_history_row(image_filename, result, created_at) for result in results]
        )


def get_recent_scans(limit=25):
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                image_filename,
                code_type,
                decoded_data,
                category,
                safety_level,
                safety_score,
                action,
                ai_summary,
                created_at
            FROM scans
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()

    return [dict(row) for row in rows]


def _build_history_row(image_filename, result, created_at):
    safety = result.get("safety") or {}
    agent = result.get("agent") or {}

    return (
        image_filename,
        result.get("type", ""),
        result.get("data", ""),
        agent.get("category", ""),
        safety.get("level", ""),
        safety.get("score", 0),
        agent.get("action", ""),
        result.get("ai", ""),
        created_at,
    )


def _connect():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection
