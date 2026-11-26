"""Datos de una página de detalle; validación antes de persistir."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Book:
    upc: str
    title: str
    category: str
    price_gbp: Decimal
    rating: int
    stock: int
    url: str
    extracted_at: datetime

    def __post_init__(self) -> None:
        if not all(value.strip() for value in (self.upc, self.title, self.category, self.url)):
            raise ValueError("UPC, título, categoría y URL son obligatorios")
        if not self.price_gbp.is_finite() or self.price_gbp < 0:
            raise ValueError("El precio debe ser finito y no negativo")
        if self.price_gbp != self.price_gbp.quantize(Decimal("0.01")):
            raise ValueError("El precio debe expresarse con precisión de peniques")
        if type(self.rating) is not int or not 1 <= self.rating <= 5:
            raise ValueError("El rating debe ser un entero entre 1 y 5")
        if type(self.stock) is not int or self.stock < 0:
            raise ValueError("El stock debe ser un entero no negativo")
        if self.extracted_at.utcoffset() is None:
            raise ValueError("La fecha de extracción debe incluir zona horaria")
