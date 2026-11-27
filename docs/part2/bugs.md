# Parte 2 — Registro de bugs

Código original en `reference/shipping_agent_original.py`. Código corregido en
`src/forge_interview/messaging/agent.py`. Tests en `tests/part2/test_messaging_acceptance.py`.

| ID | Función | Bug | Consecuencia en producción | Corrección aplicada |
| --- | --- | --- | --- | --- |
| B01 | `enviar` | `numero.bloqueado == True` — comparación en lugar de asignación | El bloqueo nunca se registra; el número bloqueado sigue rotando indefinidamente | Cambiar `==` a `=` |
| B02 | `enviar` | `enviados_hoy += 1` y `return True` fuera del `try` | Se consume cuota y se reporta éxito aunque el envío haya fallado con excepción | Mover ambas líneas dentro del `try`; añadir `return False` en el `except` |
| B03 | `enviar` | `ultimo_dia` no se actualiza tras el reset de medianoche | La siguiente llamada del mismo día resetea el contador nuevamente, permitiendo más de 25 envíos en el día | Añadir `numero.ultimo_dia = hoy` tras el reset del contador |
| B04 | `elegir_numero` | No filtra números bloqueados; usa `<= LIMITE_DIARIO` en lugar de `< LIMITE_DIARIO` | (1) Los bloqueados se siguen seleccionando. (2) Off-by-one: permite el envío 26 antes de agotarse | Añadir `not n.bloqueado` al filtro; cambiar `<=` a `<`; devolver `None` cuando la lista queda vacía |
| B05 | `normalizar` | Ambas ramas devuelven `tel` sin modificación | `"900000001"` y `"+51 900-000-001"` quedan con distinto formato; el mismo contacto recibe dos mensajes | Canonicalizar a `+51XXXXXXXXX`: strip de espacios/guiones, luego añadir prefijo si falta |
| B06 | `campana` | `time.sleep` fuera del `for` — una sola pausa al final | No hay throttling entre envíos; WhatsApp puede detectar el volumen y bloquear | Indentar dentro del bucle |
| B07 | `campana` | No deduplica contactos por número normalizado | El mismo destinatario con dos formatos distintos recibe múltiples mensajes | Añadir conjunto `vistos` antes del bucle; saltar contactos cuyo `tel_norm` ya fue procesado |

## Tests de aceptación

Todos en `tests/part2/test_messaging_acceptance.py` usando `MockAPI`:

- `test_sender_cannot_exceed_25_successful_messages` — ningún número supera 25 envíos al día.
- `test_blocked_sender_is_removed_from_rotation` — un número bloqueado no vuelve a elegirse y el fallo no cuenta como envío.
- `test_repeated_contact_receives_one_message` — el mismo destino con dos formatos distintos recibe un solo mensaje.

## Bonus — observabilidad

Métrica a añadir: contador `blocked_numbers_total` (Prometheus/StatsD) que se incrementa cada vez que `enviar` atrapa una excepción con `"blocked"`. Una alerta al superar 1 bloqueo en la última hora avisa antes de que el cliente note la caída de capacidad.
