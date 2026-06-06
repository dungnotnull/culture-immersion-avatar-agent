import asyncio
import aiosqlite
from typing import Optional
from src.core.logger import logger

class CultureCache:
    def __init__(self, db_path: str = "culture_cache.db"):
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS culture_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    term TEXT NOT NULL,
                    language TEXT NOT NULL,
                    explanation TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(term, language)
                )
            """)
            await db.commit()

    async def get(self, term: str, language: str) -> Optional[str]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT explanation FROM culture_cache WHERE term = ? AND language = ?", 
                (term, language)
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else None

    async def set(self, term: str, language: str, explanation: str):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR REPLACE INTO culture_cache (term, language, explanation) VALUES (?, ?, ?)",
                (term, language, explanation)
            )
            await db.commit()
