from dataclasses import replace
from datetime import timedelta, timezone
from decimal import Decimal

import pytest

from forge_interview.books.storage import BookStore


def test_upsert_same_upc_updates_instead_of_duplicating(tmp_path, sample_book):
    with BookStore(tmp_path / "books.sqlite3") as store:
        store.upsert(sample_book)
        store.upsert(replace(sample_book, title="Título corregido", stock=7))
        assert store.count() == 1
        saved = store.find(sample_book.upc)
        assert saved.title == "Título corregido"
        assert saved.stock == 7


def test_confirmed_record_survives_reopening(tmp_path, sample_book):
    path = tmp_path / "nested" / "books.sqlite3"
    with BookStore(path) as store:
        store.upsert(sample_book)
    with BookStore(path) as reopened:
        assert reopened.count() == 1
        assert reopened.contains_url(sample_book.url)
        assert reopened.find(sample_book.upc) == sample_book


def test_money_and_timestamp_round_trip_without_losing_precision(tmp_path, sample_book):
    local_date = sample_book.extracted_at.astimezone(timezone(timedelta(hours=-5)))
    book = replace(sample_book, price_gbp=Decimal("0.29"), extracted_at=local_date)
    with BookStore(tmp_path / "books.sqlite3") as store:
        store.upsert(book)
        saved = store.find(book.upc)
    assert saved.price_gbp == Decimal("0.29")
    assert saved.extracted_at == local_date
    assert saved.extracted_at.utcoffset() == timedelta(0)


@pytest.mark.parametrize("field,value", [("stock", -1), ("rating", 6)])
def test_invalid_book_is_rejected_before_persistence(sample_book, field, value):
    with pytest.raises(ValueError):
        replace(sample_book, **{field: value})
