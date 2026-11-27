# 1Forge · Prueba técnica de Product Owner de Agentes IA

Arturo Alvarez de la Torre

| Parte | Entrega |
| --- | --- |
| 1. Scraper | Catálogo de libros en SQLite, con reanudación, backoff y logs. |
| 2. Debugging | [Agente corregido](src/forge_interview/messaging/agent.py), [registro de bugs](docs/part2-bugs.md) y pruebas con MockAPI. |
| 3. Diseño | [Agente de enriquecimiento](docs/part3-enrichment.md), con flujo, validación, evaluación y costos. |
| 4. Producto | [Plan semanal para Nemo](docs/part4-product.md), mensaje al cliente y propuesta comercial. |

## Instalación

Python 3.11 o superior. El scraper necesita Internet para acceder a [Books to Scrape](https://books.toscrape.com/). Las pruebas se ejecutan offline.

```bash
python -m venv .venv
# macOS o Linux
source .venv/bin/activate
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest -q
```

En Windows, también puedes ejecutar `.\.venv\Scripts\python.exe` en lugar de `python` sin activar el entorno.

## Demo y ejecución completa

Para la demo, parte de una base nueva. Cambia el nombre del archivo si ya usaste esta ruta.

```bash
python -m forge_interview.books scrape --db data/demo.sqlite3 --limit 3 --delay 0.5
python -m forge_interview.books scrape --db data/demo.sqlite3 --limit 5 --delay 0.5
python -m forge_interview.books scrape --db data/demo.sqlite3 --limit 5 --delay 0.5
python -m forge_interview.books status --db data/demo.sqlite3
```

`--limit` fija el **total objetivo en SQLite**. La segunda ejecución vuelve al listado, omite tres detalles y guarda dos nuevos. La tercera termina con cinco filas y sin solicitudes. Para una extracción completa:

```bash
python -m forge_interview.books scrape --db data/books.sqlite3 --delay 1.5
```

Si interrumpes con Ctrl+C, repite el mismo comando con la misma base. El scraper reanuda a partir de los detalles ya confirmados. El comando instalado `forge-books` es equivalente a `python -m forge_interview.books`.

## Decisiones del scraper

- **Identidad y reanudación.** UPC es la clave primaria en SQLite. Cada escritura se confirma individualmente. Al retomar se recorre el listado desde la primera página y se consulta el índice por URL antes de pedir cada detalle. Los detalles guardados son una captura y conservan su fecha, su precio y su stock durante la reanudación.
- **Extracción.** Título, categoría, precio, rating, UPC y stock salen del detalle. SQLite guarda GBP en peniques enteros y el instante de extracción en UTC. Si el HTML no cumple el contrato, queda un error con la URL y el registro se recupera en una ejecución posterior.
- **Red.** El proceso es secuencial. `--delay` es la pausa mínima después de cada petición y también aplica a reintentos. Errores de red y HTTP 5xx se reintentan hasta `--max-retries` veces, con backoff de 1, 2 y 4 s bajo las opciones por defecto y una pausa efectiva igual al máximo entre el backoff y el delay. Cada intento tiene `--timeout`. Un HTTP 401, 403 o 429 detiene el flujo.
- **Estado.** Los logs muestran detalles guardados, omitidos, errores y duración. La CLI devuelve 1 si faltan libros o se corta el catálogo por error, y 130 si lo interrumpe el usuario.

### Bonus SQL · Categorías con más stock

```sql
SELECT category, SUM(stock) AS total_stock
FROM books
GROUP BY category
ORDER BY total_stock DESC, category ASC
LIMIT 5;
```

## Verificación

- Python 3.12, `pytest` y Ruff. Las pruebas cubren selectores críticos, paginación, interrupción, reanudación, idempotencia, reintentos y el agente con MockAPI.
- En el sitio real se validó el recorrido 3 → 5 → 5 sobre la misma base. El agente de envíos usa el mock y el diseño de enriquecimiento está en Markdown.
- La ventana horaria y Selenium son extras opcionales fuera del alcance entregado.

Para la revisión en vivo, consulta [el guion de demo](docs/review.md).
