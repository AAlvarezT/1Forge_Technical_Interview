"""Recorre el catálogo y confirma cada libro válido en SQLite."""

import logging
import math
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .parser import parse_book_detail
from .storage import BookStore

CATALOG_URL = "https://books.toscrape.com/"
logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ScraperConfig:
    db: Path
    delay: float = 1.5
    max_retries: int = 3
    timeout: float = 30.0
    limit: int = 1000

    def __post_init__(self) -> None:
        if not math.isfinite(self.delay) or self.delay < 0:
            raise ValueError("delay debe ser finito y no negativo")
        if not math.isfinite(self.timeout) or self.timeout <= 0:
            raise ValueError("timeout debe ser finito y positivo")
        if self.max_retries < 0:
            raise ValueError("max-retries debe ser no negativo")
        if not 1 <= self.limit <= 1000:
            raise ValueError("limit debe estar entre 1 y 1000")


class CatalogClient:
    def __init__(self, session: requests.Session, config: ScraperConfig) -> None:
        self.session = session
        self.config = config
        self.request_started = False

    def get_html(self, url: str) -> str:
        for attempt in range(self.config.max_retries + 1):
            if self.request_started:
                backoff = 2 ** min(attempt - 1, 5) if attempt else 0
                time.sleep(max(self.config.delay, backoff))
            self.request_started = True

            try:
                response = self.session.get(url, timeout=self.config.timeout)
                response.raise_for_status()
            except requests.HTTPError as error:
                if not 500 <= error.response.status_code < 600:
                    raise
                failure = error
            except (
                requests.ConnectionError,
                requests.Timeout,
                requests.exceptions.ChunkedEncodingError,
            ) as error:
                failure = error
            else:
                return response.content.decode("utf-8")

            if attempt == self.config.max_retries:
                raise failure
            logger.warning("Reintento %d para %s: %s", attempt + 1, url, failure)

        raise AssertionError("Se esperaba un intento de conexión")


def run_scraper(config: ScraperConfig) -> int:
    """Devuelve el total persistido. El límite es el total objetivo en la base."""
    started_at = time.monotonic()
    added = skipped = errors = 0
    page_url = CATALOG_URL
    visited = set()
    with BookStore(config.db) as store, requests.Session() as session:
        client = CatalogClient(session, config)
        total = store.count()
        try:
            while page_url and total < config.limit:
                if page_url in visited:
                    raise ValueError(f"Paginación circular en {page_url}")
                visited.add(page_url)
                soup = BeautifulSoup(client.get_html(page_url), "html.parser")
                links = soup.select("article.product_pod h3 a[href]")
                if not links:
                    raise ValueError(f"El listado no contiene enlaces a libros: {page_url}")
                for link in links:
                    url = urljoin(page_url, link["href"])
                    if store.contains_url(url):
                        skipped += 1
                        continue
                    try:
                        book = parse_book_detail(client.get_html(url), url)
                    except requests.HTTPError as error:
                        if error.response.status_code in {401, 403, 429}:
                            raise
                        logger.error("Detalle %s: %s", url, error)
                        errors += 1
                        continue
                    except (requests.RequestException, ValueError) as error:
                        logger.error("Detalle %s: %s", url, error)
                        errors += 1
                        continue
                    store.upsert(book)
                    total = store.count()
                    added += 1
                    if total >= config.limit:
                        break

                logger.info(
                    "Listado %d | guardados=%d/%d | omitidos=%d | errores=%d",
                    len(visited),
                    total,
                    config.limit,
                    skipped,
                    errors,
                )
                next_link = soup.select_one("li.next a[href]")
                page_url = urljoin(page_url, next_link["href"]) if next_link else None
        except (requests.RequestException, ValueError):
            errors += 1
            raise
        finally:
            logger.info(
                "Fin | total SQLite=%d | detalles guardados=%d | omitidos=%d | errores=%d | %.1f s",
                total,
                added,
                skipped,
                errors,
                time.monotonic() - started_at,
            )
    return total
