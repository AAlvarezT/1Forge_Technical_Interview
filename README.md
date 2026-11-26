# 1FORGE - Prueba técnica

Repositorio de Arturo Alvarez de la Torre para la prueba de Product Owner de Agentes IA.

## Estado actual: scaffolding

Esta versión prepara el proyecto. **No es todavía la solución final ni una entrega completa.**

| Parte | Preparado | Pendiente |
| --- | --- | --- |
| 1. Scraper | Modelo de libro, SQLite con UPC como clave, comandos y pruebas de persistencia. | Parsing, paginación, red, reintentos, pausas y ejecución real de los 1,000 libros. |
| 2. Debugging | Código original, copia de trabajo, MockAPI y tres pruebas de aceptación. | Corregir bugs, retirar los `xfail` al resolverlos y documentar cambios. |
| 3. Diseño | Plantilla con arquitectura, harness, validación, diagnóstico, costos y métricas. | Completar y justificar el diseño en 1-2 páginas más diagrama. |
| 4. Producto | Los seis pendientes y plantilla de priorización, mensaje e idea de producto. | Decidir prioridades, esfuerzos y alcance semanal. |

Los tests `xfail` son **requisitos pendientes que fallan en el código original**. No cuentan como funcionalidad terminada. Con `strict=True`, un test que comience a pasar exige retirar su marca.

## Instalación

Se requiere Python 3.11 o superior. SQLite forma parte de la biblioteca estándar.

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell (alternativa al comando anterior)
# .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Comandos disponibles

```bash
forge-books --help
forge-books init-db --db data/books.sqlite3
forge-books status --db data/books.sqlite3
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
```

La base se crea al ejecutar `init-db`; los datos y las credenciales quedan fuera de Git.

El contrato del scraper está preparado:

```bash
forge-books scrape --db data/books.sqlite3 --delay 1.5 --max-retries 3 --timeout 30
```

**Este último comando todavía termina con código 2 y un mensaje de pendiente.** No realiza peticiones ni afirma haber descargado libros. `--limit 10` servirá para una ejecución pequeña cuando se implemente el recorrido.

También se puede ejecutar la CLI con `python -m forge_interview.books`.

## Verificación de esta base

Comprobado con Python 3.12:

- Instalación editable del paquete y resolución de sus dependencias.
- `pytest`: **5 aprobados y 3 fallos esperados (`xfail`)** del agente original.
- Ruff: análisis y formato aprobados.
- CLI: ayuda, creación de esquema, estado y rechazo de parámetros inválidos.
- `scrape`: salida de pendiente con código 2, sin peticiones de red.

Estos resultados validan el scaffolding y la persistencia. Todavía no validan la
extracción de 1,000 libros ni un agente corregido.

## Organización

| Ruta | Propósito |
| --- | --- |
| `src/forge_interview/books/` | Modelo, persistencia, configuración y puntos de entrada del scraper. |
| `src/forge_interview/messaging/agent.py` | Copia de trabajo del agente, todavía con los bugs del enunciado. |
| `src/forge_interview/messaging/mock_api.py` | Mock local del enunciado; no envía mensajes reales. |
| `reference/shipping_agent_original.py` | Código original para comparar cambios. |
| `tests/` | Pruebas offline de persistencia y contratos del agente. |
| `docs/requirements.md` | Lista de requisitos y evidencias por completar. |
| `docs/part2-bugs.md` | Registro de bugs, consecuencias y correcciones. |
| `docs/part3-enrichment.md` | Diseño del agente de enriquecimiento. |
| `docs/part4-product.md` | Priorización, comunicación e idea de producto. |
| `docs/review.md` | Guion y verificaciones para la revisión en vivo. |

## Decisiones iniciales

- **Pocos componentes:** requests y Beautiful Soup para el sitio estático. Selenium queda como dependencia opcional para el bonus con JavaScript.
- **Dinero sin flotantes:** el modelo usa `Decimal`; SQLite guarda el precio en peniques enteros (`price_pence`). La moneda es GBP para este ejercicio.
- **Persistencia por registro:** cada `upsert` confirmado se guarda en una transacción. Esto prepara la reanudación después de una interrupción.
- **UPC como identidad:** el UPC es la clave primaria. `contains_url()` permitirá evitar volver a pedir páginas de detalle ya guardadas.
- **Fecha explícita:** las extracciones se registran con zona horaria y se normalizan a UTC al guardar.
- **Red y envíos separados de los tests:** las verificaciones iniciales no hacen scraping real ni contactan a WhatsApp.
- **Alcance honesto:** la persistencia implementa una base para la idempotencia; la reanudación integral solo quedará demostrada cuando exista el recorrido y se pruebe una interrupción.

## Siguiente trabajo

1. Implementar `parse_book_detail()` con una página de detalle de prueba.
2. Implementar `run_scraper()`: descubrir URLs, revisar `contains_url()`, descargar, validar y guardar.
3. Añadir reintentos limitados, pausa configurable y logs de progreso y duración.
4. Depurar el agente con cambios mínimos y convertir los tres `xfail` en tests aprobados.
5. Completar partes 3 y 4 y ensayar cambios pequeños en vivo.

## Entrega

- Un repositorio público o privado con acceso para el evaluador.
- Partes 1 y 2 ejecutables, tests y README con decisiones y limitaciones.
- Partes 3 y 4 en Markdown dentro de `docs/` (formato permitido por el enunciado).
- Documentar qué quedó incompleto y el uso de IA. Cada línea entregada debe poder explicarse y modificarse en vivo.

Antes de enviar, seguir [la lista de revisión](docs/review.md).
