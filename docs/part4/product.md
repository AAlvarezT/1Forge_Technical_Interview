# Parte 4 — Caso de producto con Nemo Contact Center

Capacidad disponible: **15 horas de ingeniería esta semana**.

---

## 1. Priorización

| Pos. | ID | Pendiente | Horas est. | Esta semana | Justificación |
|---|---|---|---|---|---|
| 1 | **A** | 4 de 20 números bloqueados; chips toman 2 días | 2 h | ✅ Sí | Emergencia operativa — 20% de capacidad perdida. Arrancar el trámite hoy para tener chips antes del miércoles. |
| 2 | **B** | Claro advirtió por volumen de consultas | 4 h | ✅ Sí | Riesgo alto: una segunda advertencia puede terminar en bloqueo de IP o suspensión de acceso, lo que detiene la extracción de datos completamente. |
| 3 | **D** | 30% de rebote en mailing | 3 h | ✅ Sí | Un rebote tan alto quema la reputación del dominio en pocas campañas. Limpiar la lista y verificar SPF/DKIM/DMARC antes de enviar el siguiente batch. |
| 4 | **E** | hCaptcha de OSIPTEL bloquea IP una vez/semana | 4 h | ✅ Sí | Interrumpe la extracción semanal. Con rotación de IP o proxy residencial queda resuelto; entra dentro del tiempo disponible. |
| 5 | **F** | Agente que responda automáticamente al WhatsApp | — | 🔜 Próx. sprint | Feature nuevo de ~8–12 h de diseño + desarrollo. Alto valor para Nemo pero no hay emergencia; hacerlo bien es mejor que apresurado. |
| 6 | **C** | Dashboard de respuestas de WhatsApp | — | 🔜 Próx. sprint | Visibilidad para el cliente, no bloquea operaciones. Entra en el sprint siguiente junto con F. |

**Total comprometido esta semana: 13 h** (dentro del límite de 15 h, dejando 2 h de colchón).  
**Fuera de esta semana:** F y C. Ambos son mejoras de producto sin urgencia operativa; comprometerlos esta semana sacaría A, B o D del alcance y eso tiene más riesgo real.

---

## 2. Mensaje al gerente de Nemo

> Hola, te mando el plan de la semana 👋
>
> ✅ **A** — Arrancamos hoy el trámite de los 4 chips nuevos; deberían estar activos antes del miércoles.
> ✅ **B** — Reducimos la frecuencia de consultas a Claro y activamos rotación para bajar el volumen; evitamos la siguiente advertencia.
> ✅ **D** — Limpiamos la lista de mailing y revisamos la configuración de envío para bajar el rebote del 30%.
> ✅ **E** — Implementamos rotación de IP para que el hCaptcha de OSIPTEL deje de bloquearnos.
>
> 🔜 El dashboard (C) y el agente de respuesta automática (F) los arrancamos la semana que viene — necesitan diseño y no quiero apresurarlos con solo 15 h disponibles.
>
> ¿Hay algo que quieras mover de prioridad?

---

## 3. Idea de nuevo producto

**Cliente propuesto: IDAT** (Instituto de Diseño y Administración Tecnológica) — cadena de institutos técnicos peruanos con ~15 sedes en Lima y provincias, con carreras de tecnología, administración y diseño.

**Problema:** cuando un prospecto llena el formulario de admisiones en la web o escribe por WhatsApp, el seguimiento lo hacen asesores humanos que pueden tardar 24–48 horas en responder. En ese tiempo el lead se enfría, el prospecto ya habló con otro instituto, o simplemente no vuelve a contestar. La tasa de conversión de lead a matrícula es baja no por falta de interés, sino por demora en el primer contacto.

**Propuesta:** un agente de admisiones automático que, en los primeros 5 minutos tras el registro, envía un WhatsApp personalizado al prospecto, hace 2–3 preguntas de calificación (carrera de interés, si trabaja o estudia, disponibilidad de horario) y agenda una cita con un asesor humano directamente en el calendario. Los prospectos que no responden reciben un recordatorio a las 24 h y otro a los 3 días. El asesor humano solo entra cuando el lead ya está calificado y tiene una cita confirmada.

**Piezas del stack que se reusan:** rotación de números de WhatsApp con límite diario (Parte 2), extracción de catálogo de carreras desde la web de IDAT (Parte 1), LLM para personalizar los mensajes según la carrera de interés.

**Precio tentativo:** setup S/ 6,000 (integración con su CRM y configuración de flujos) + S/ 2,800/mes (operación, mantenimiento y hasta 1,500 conversaciones activas al mes).
