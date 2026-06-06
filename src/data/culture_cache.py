import sqlite3
import json
from typing import Optional
from src.core.logger import logger

class CultureCache:
    def __init__(self, db_path: str = "data/culture_cache.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS culture_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    term TEXT NOT NULL,
                    language TEXT NOT NULL,
                    explanation TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(term, language)
                )
            """)
            conn.commit()

    def get(self, term: str, language: str) -> Optional[str]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT explanation FROM culture_cache WHERE term = ? AND language = ?", (term, language))
            row = cursor.fetchone()
            return row[0] if row else None

    def set(self, term: str, language: str, explanation: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO culture_cache (term, language, explanation) VALUES (?, ?, ?)",
                (term, language, explanation)
            )
            conn.commit()
