# Parte 2 - Registro de bugs

Estado: pendiente de diagnóstico completo y corrección. El original está en
`reference/shipping_agent_original.py`; la copia de trabajo está en
`src/forge_interview/messaging/agent.py`.

| ID | Función / ubicación | Bug | Consecuencia en producción | Corrección aplicada | Test que lo demuestra | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| B01 | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | Sin resolver |

## Contratos ya preparados

- `test_sender_cannot_exceed_25_successful_messages`: límite diario y capacidad agotada.
- `test_blocked_sender_is_removed_from_rotation`: marcar bloqueo, no contar un fallo y excluirlo.
- `test_repeated_contact_receives_one_message`: mismo destinatario con formatos distintos.

Actualmente son `xfail(strict=True)` porque el original tiene esos fallos. Retirar
cada marca al implementar la corrección. Ampliar las pruebas cuando el diagnóstico
identifique otros casos de fallo importantes.

## Decisiones que habrá que documentar

- Qué formato de número se acepta y qué país se asume.
- Qué significa "duplicado": dentro de la campaña o también entre ejecuciones.
- En qué zona horaria cambia el día y dónde se actualiza ese estado.
- Qué sucede si no quedan números disponibles o si la API falla.
- Cuándo se considera exitoso un envío y cuándo se incrementa el contador.

## Bonus de observabilidad

Pendiente: definir evento de bloqueo, métrica, umbral y destinatario de la alerta.
El ejercicio se verificará exclusivamente con MockAPI.
