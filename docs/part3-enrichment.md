# Parte 3 - Diseño del agente de enriquecimiento

**Plantilla pendiente.** Versión final: 1-2 páginas de texto más un diagrama.
No se pide implementar ni ejecutar búsquedas de contactos en esta parte.

## 1. Arquitectura

Pendiente: diagrama de entrada RUC -> fuentes autorizadas -> evidencia ->
intervención del LLM -> validación -> contacto corporativo validado o descarte.
Indicar qué hace cada herramienta, qué guarda y dónde interviene una persona.

## 2. Harness del agente

| Componente | Decisión y justificación |
| --- | --- |
| Herramientas disponibles y límites | Pendiente |
| Contexto entregado al LLM | Pendiente |
| Esquema de salida y evidencia de fuente | Pendiente |
| Validación de la respuesta | Pendiente |
| Presupuesto de intentos / costo / tiempo | Pendiente |
| Ausencia de evidencia, errores y revisión humana | Pendiente |

## 3. Validación y confianza

Pendiente: definir evidencia de la relación entre empresa y contacto corporativo.
Un número con formato válido o prefijo coincidente no acredita titularidad.
Explicar cómo se asigna confianza y cuándo se descarta un resultado.

## 4. Diagnóstico del baseline

El caso reporta 5% en 500 empresas: 25 hallazgos válidos según su definición actual.
Pendiente: confirmar cómo se etiquetó la validez y trabajar tres hipótesis comprobables.

| Hipótesis | Cómo comprobarla | Evidencia que la confirmaría o descartaría |
| --- | --- | --- |
| 1. Pendiente | Pendiente | Pendiente |
| 2. Pendiente | Pendiente | Pendiente |
| 3. Pendiente | Pendiente | Pendiente |

## 5. Costos

Presupuesto total aprobado: **US$1,000, incluyendo desarrollo y operación**.

- `presupuesto_operativo = 1000 - costo_desarrollo`
- `costo_empresa = costo_busquedas + costo_tokens_entrada + costo_tokens_salida + otros_costos`
- `empresas_procesables = floor(presupuesto_operativo / costo_empresa)` si ambos son positivos.

Pendiente: elegir proveedores, verificar precios en fuentes oficiales, fechar las
tarifas y declarar volumen esperado de búsquedas, tokens y reintentos. Incluir un
escenario de costos y aclarar qué rubros no estén contemplados.

## 6. Métricas

Pendiente: distinguir cobertura de precisión, resultados descartados, costo por
contacto validado y errores. Comparar sobre una muestra con el mismo criterio de
validez y evitar presentar una mejora esperada como un resultado observado.

## Riesgos legales o de cumplimiento (2-3 líneas)

Pendiente: verificar fuentes oficiales peruanas antes de completar el texto.
Delimitar fuentes autorizadas, datos corporativos y tratamiento de datos personales.
