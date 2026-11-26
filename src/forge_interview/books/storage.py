"""Persistencia local. El UPC identifica al libro y cada escritura se confirma."""

import sqlite3
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from .models import Book

SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
    upc TEXT PRIMARY KEY NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    price_pence INTEGER NOT NULL CHECK (price_pence >= 0),
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    stock INTEGER NOT NULL CHECK (stock >= 0),
    url TEXT NOT NULL,
    extracted_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_books_url ON books(url);
"""


class BookStore:
    def __init__(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(path)
        self._connection.row_factory = sqlite3.Row
        self._connection.executescript(SCHEMA)

    def __enter__(self) -> "BookStore":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._connection.close()

    def upsert(self, book: Book) -> None:
        with self._connection:
            self._connection.execute(
                """
                INSERT INTO books
                    (upc, title, category, price_pence, rating, stock, url, extracted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(upc) DO UPDATE SET
                    title=excluded.title,
                    category=excluded.category,
                    price_pence=excluded.price_pence,
                    rating=excluded.rating,
                    stock=excluded.stock,
                    url=excluded.url,
                    extracted_at=excluded.extracted_at
                """,
                (
                    book.upc,
                    book.title,
                    book.category,
                    int(book.price_gbp * 100),
                    book.rating,
                    book.stock,
                    book.url,
                    book.extracted_at.astimezone(timezone.utc).isoformat(timespec="seconds"),
                ),
            )

    def contains_url(self, url: str) -> bool:
        return (
            self._connection.execute("SELECT 1 FROM books WHERE url = ? LIMIT 1", (url,)).fetchone()
            is not None
        )

    def count(self) -> int:
        return self._connection.execute("SELECT COUNT(*) FROM books").fetchone()[0]

    def find(self, upc: str) -> Book | None:
        row = self._connection.execute("SELECT * FROM books WHERE upc = ?", (upc,)).fetchone()
        if row is None:
            return None
        return Book(
            upc=row["upc"],
            title=row["title"],
            category=row["category"],
            price_gbp=Decimal(row["price_pence"]) / 100,
            rating=row["rating"],
            stock=row["stock"],
            url=row["url"],
            extracted_at=datetime.fromisoformat(row["extracted_at"]),
        )
