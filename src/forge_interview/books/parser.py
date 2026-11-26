"""Punto de implementación del parser de detalle. Pendiente en el scaffolding."""

from .models import Book


def parse_book_detail(html: str, url: str) -> Book:
    """Extraer título, categoría, precio, rating, UPC, stock y fecha UTC.

    Leer la categoría del breadcrumb y el UPC de la tabla de producto.
    Fallar con un mensaje útil si falta un campo obligatorio; evitar guardar
    datos parciales como si fueran un libro correcto.
    """
    raise NotImplementedError("Pendiente: parser de la página de detalle")
