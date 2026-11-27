"""Extrae los campos obligatorios del HTML de detalle."""

import re
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

from bs4 import BeautifulSoup

from .models import Book

RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def parse_book_detail(html: str, url: str) -> Book:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.select_one(".product_main h1")
    price = soup.select_one(".product_main .price_color")
    stars = soup.select_one(".product_main .star-rating")
    category = soup.select_one(".breadcrumb li:nth-last-child(2) a")
    info = {}
    for row in soup.select(".table-striped tr"):
        label, value = row.find("th"), row.find("td")
        if label is not None and value is not None:
            info[label.get_text(strip=True)] = value.get_text(strip=True)

    if title is None or price is None or stars is None or category is None:
        raise ValueError("Faltan título, precio, rating o categoría en el HTML")
    if not info.get("UPC"):
        raise ValueError("Falta el UPC en la tabla de producto")
    stock_text = info.get("Availability", "")
    available = re.fullmatch(r"In stock\s*\((\d+)\s+available\)", stock_text)
    if available:
        stock = int(available.group(1))
    elif stock_text == "Out of stock":
        stock = 0
    else:
        raise ValueError(f"Disponibilidad no reconocida: {stock_text!r}")

    ratings = [RATINGS[name] for name in stars.get("class", []) if name in RATINGS]
    if len(ratings) != 1:
        raise ValueError("El rating debe tener una sola clase reconocida")

    price_text = price.get_text(strip=True)
    if not price_text.startswith("£"):
        raise ValueError(f"Precio fuera del formato GBP: {price_text!r}")
    try:
        price_gbp = Decimal(price_text[1:])
        return Book(
            upc=info["UPC"],
            title=title.get_text(strip=True),
            category=category.get_text(strip=True),
            price_gbp=price_gbp,
            rating=ratings[0],
            stock=stock,
            url=url,
            extracted_at=datetime.now(timezone.utc),
        )
    except InvalidOperation as error:
        raise ValueError(f"Precio inválido: {price_text!r}") from error
