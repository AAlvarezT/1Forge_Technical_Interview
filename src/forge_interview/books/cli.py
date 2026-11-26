"""Comandos de inicialización y punto de entrada para el scraper."""

import argparse
import logging
from pathlib import Path

from .scraper import ScraperConfig, run_scraper
from .storage import BookStore


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Parte 1: libros y persistencia SQLite")
    commands = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (
        ("init-db", "Crear o abrir el esquema de SQLite"),
        ("status", "Mostrar cuántos libros hay guardados"),
        ("scrape", "Ejecutar el scraper (implementación pendiente)"),
    ):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("--db", type=Path, default=Path("data/books.sqlite3"))
        if name == "scrape":
            command.add_argument("--delay", type=float, default=1.5)
            command.add_argument("--max-retries", type=int, default=3)
            command.add_argument("--timeout", type=float, default=30.0)
            command.add_argument("--limit", type=int, default=1000)

    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    if args.command in {"init-db", "status"}:
        with BookStore(args.db) as store:
            print(f"Base: {args.db} | Libros guardados: {store.count()}")
        return 0

    try:
        config = ScraperConfig(
            db=args.db,
            delay=args.delay,
            max_retries=args.max_retries,
            timeout=args.timeout,
            limit=args.limit,
        )
    except ValueError as error:
        parser.error(str(error))
    try:
        run_scraper(config)
    except NotImplementedError as error:
        logging.error("%s", error)
        return 2
    return 0
