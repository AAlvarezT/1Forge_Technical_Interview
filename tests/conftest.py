"""Datos sintéticos para pruebas offline; no corresponden a libros extraídos."""

from datetime import datetime, timezone
from decimal import Decimal

import pytest

from forge_interview.books.models import Book


@pytest.fixture
def sample_book():
    return Book(
        upc="0123456789abcdef",
        title="Libro sintético de prueba",
        category="Pruebas",
        price_gbp=Decimal("12.34"),
        rating=4,
        stock=22,
        url="https://example.com/catalogue/libro-de-prueba/index.html",
        extracted_at=datetime(2026, 11, 25, 23, 0, tzinfo=timezone.utc),
    )
