"""Contrato de ejecución. El recorrido y las peticiones se implementan después."""

import math
from dataclasses import dataclass
from pathlib import Path


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


def run_scraper(config: ScraperConfig) -> int:
    """Devolver el total persistido al completar el recorrido.

    Pendiente:
    1. Recorrer los listados de books.toscrape.com con URLs absolutas.
    2. Saltar las páginas de detalle presentes en BookStore.contains_url().
    3. Usar timeout, delay configurable y reintentos limitados con backoff.
    4. Parsear y confirmar cada libro válido con BookStore.upsert().
    5. Registrar progreso, errores, duración y resultado de la ejecución.

    La reanudación de extremo a extremo debe probarse con una interrupción.
    """
    raise NotImplementedError("Pendiente: recorrido, peticiones, reintentos y logs del scraper")
