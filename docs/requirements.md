# Requisitos y evidencias

Fuente: enunciado de seis páginas recibido el 25 de noviembre de 2026.
Estado de este documento: scaffolding. Las casillas vacías son trabajo pendiente.

## Parte 1 - Scraper

- [ ] Extraer 1,000 libros desde las páginas de detalle de books.toscrape.com.
- [ ] Obtener título, categoría, precio, rating 1-5, UPC, stock entero, URL y fecha/hora.
- [x] Preparar esquema SQLite con UPC como clave y escritura sin duplicados.
- [ ] Demostrar idempotencia del recorrido completo con dos ejecuciones.
- [ ] Demostrar interrupción y reanudación sin volver a extraer detalles guardados.
- [ ] Aplicar `--delay` entre requests (incluidos detalles y reintentos).
- [ ] Reintentar errores de red y 5xx con backoff y un límite de intentos.
- [ ] Registrar libros procesados, errores y tiempo total.
- [ ] Completar README con instrucciones probadas y decisiones.

Bonus, después de lo obligatorio:

- [ ] Ventana horaria configurable.
- [ ] quotes.toscrape.com/js con Selenium headless.
- [ ] SQL de cinco categorías con más stock total.

## Parte 2 - Debugging

- [x] Conservar una transcripción del original y una copia de trabajo.
- [x] Preparar MockAPI y tres contratos de aceptación que muestran fallos conocidos.
- [ ] Enumerar cada bug, ubicación, consecuencia y corrección.
- [ ] Aplicar cambios mínimos al agente.
- [ ] Aprobar el test de límite diario sin `xfail`.
- [ ] Aprobar el test de exclusión de bloqueados sin `xfail`.
- [ ] Aprobar el test de destinatarios duplicados sin `xfail`.
- [ ] Verificar cambio de día, falta de emisores y errores de la API.
- [ ] Bonus: proponer métrica o alerta de bloqueo.

## Parte 3 - Solo diseño

- [ ] Arquitectura: entrada RUC y salida validada o descartada, con fuentes y herramientas.
- [ ] Harness: herramientas del LLM, contexto, validación y manejo de fallos.
- [ ] Evidencia de relación empresa-contacto y niveles de confianza.
- [ ] Tres hipótesis comprobables sobre el 5% actual (25 de 500 empresas).
- [ ] Costos por empresa y presupuesto de US$1,000 que incluye desarrollo y operación.
- [ ] Métricas de evaluación comparables con el baseline.
- [ ] Riesgos legales/de cumplimiento en Perú en 2-3 líneas, con fuentes verificadas.
- [ ] Documento de 1-2 páginas más un diagrama.

## Parte 4 - Producto

- [ ] Ordenar los seis pendientes por impacto, riesgo y esfuerzo.
- [ ] Respetar 15 horas de ingeniería disponibles en la semana.
- [ ] Explicitar qué queda fuera.
- [ ] Mensaje al gerente de Nemo de máximo ocho líneas.
- [ ] Una empresa peruana mediana de otro rubro y un agente comercial en un párrafo.
- [ ] Incluir componentes reutilizables, setup y mensualidad tentativos.

## Entrega y revisión

- [ ] Repositorio accesible para el evaluador; confirmar su usuario si permanece privado.
- [ ] Instalación desde un entorno limpio y ejecución con los comandos del README.
- [ ] Tests aprobados y pendientes restantes identificados con honestidad.
- [ ] Partes 3 y 4 dentro del mismo repo.
- [ ] Explicar y modificar lo entregado sin depender de generar una solución nueva en vivo.
