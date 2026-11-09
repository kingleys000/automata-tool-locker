# Guion para sustentar los avances 3 4 y 5

Duración orientativa: 12 minutos, ajustable a la indicación docente. Distribuir intervenciones por roles y ensayar la presentación completa con todos los integrantes.

| Tiempo | Tema | Explicación y soporte |
|---|---|---|
| 0–1 min | Problema y alcance | Formular la necesidad de trazabilidad. Precisar una herramienta, contexto por validar y hardware simulado. |
| 1–3 min | Metodología | Explicar fases, objetivos, productos y cronograma del avance 3. Mostrar qué evidencia se obtiene en cada fase. |
| 3–5 min | Análisis | Presentar actores, proceso, requisitos verificables y caso de uso de devolución. Referir la evidencia de campo cuando exista. |
| 5–8 min | Diseño | Recorrer arquitectura, estados, modelo de datos y pantallas. Explicar cómo cada parte responde a requisitos. |
| 8–10 min | Demostración | Mostrar un ciclo del simulador y un rechazo. Nombrar explícitamente que la escena y sus observaciones son simuladas. |
| 10–12 min | Evidencia y siguiente hito | Presentar pruebas automatizadas y pendientes de dataset, evaluación y ciclos con cámara. |

## Demostración reproducible

Iniciar el simulador con `./iniciar_simulador.sh` o `.venv/bin/python run_simulador.py`. Abrir `http://127.0.0.1:8001/simulador`. Mostrar el escenario de ciclo completo y explicar cada transición: Disponible, Reservada, Prestada, En revisión y Disponible. Mostrar el escenario de objeto incorrecto para explicar el rechazo. La vista `http://IP_DEL_COMPUTADOR:8001/automatas` permite observar ambos diagramas desde una segunda pantalla en la misma red.

El módulo visual se inicia aparte con `.venv/bin/python run.py`, puerto 8000. Solo presentarlo como reconocimiento real cuando haya cámara, modelo y evidencias válidas. Si falta el modelo, mostrar el bloqueo y explicar la condición pendiente. La captura de imágenes y la inferencia son actividades diferentes.

## Preguntas y respuestas para preparar

**¿Qué aporta Teoría de la Computación?** El modelo de estados explicita eventos permitidos y permite razonar sobre secuencias. El reconocedor académico acepta trazas válidas que terminan Disponible e incluye un estado absorbente Error para transiciones inválidas.

**¿Por qué dos autómatas?** Uno representa disponibilidad administrativa; otro representa apertura, espera, cierre, verificación e incidencia. Estar Disponible no autoriza por sí solo una apertura: el controlador exige condiciones adicionales.

**¿La base de datos hace infinito al autómata?** Los usuarios, fechas y registros son datos auxiliares de la aplicación. El AFD académico tiene un conjunto finito de estados y símbolos. El controlador de la aplicación añade condiciones y salidas; conviene explicar esa diferencia formal.

**¿Qué sucede con una acción inválida?** El controlador la rechaza y conserva el estado, permitiendo corregir la acción. El reconocedor de trazas completas envía un símbolo inválido a Error. Son comportamientos distintos con propósitos diferentes.

**¿La IA identifica exactamente el mismo martillo?** La clasificación evalúa apariencia de clase dentro de una escena controlada. No acredita identidad de una unidad particular ni detecta daños de forma certificada. El encargado realiza la revisión.

**¿Una confianza 0,85 significa 85 % de exactitud?** No. Es un umbral de una puntuación del modelo; la exactitud se mide sobre muestras etiquetadas reservadas para evaluación.

**¿Cómo se impide un préstamo duplicado?** El motor serializa decisiones y SQLite mantiene un índice único parcial para préstamos activos de una herramienta. Se comprueba también el reenvío idempotente de solicitudes.

**¿Por qué la devolución no termina Disponible?** Termina En revisión. El encargado decide aprobación o daño, de modo que una apariencia compatible con martillo no sustituye la inspección humana.

**¿Qué resultados se pueden defender hoy?** El código y la suite automatizada permiten demostrar reglas y escenarios controlados. La ejecución del 5 de noviembre obtuvo 47 pruebas aprobadas. Las métricas del modelo y los diez ciclos reales requieren ejecución y registro adicionales.

**¿Cómo se usó IA en estos documentos?** Codex coordinó e integró el material, Kimi desarrolló metodología y planificación, y Agy trabajó en análisis y diseño. El equipo estudiantil debe revisar y comprender los aportes, validar las afirmaciones del contexto y seguir la política docente para declarar ese apoyo.

## Preparación del equipo

Cada integrante debe poder recorrer una traza aceptada, explicar un rechazo, localizar el requisito asociado y señalar su evidencia. Ensayar preguntas con intercambio de roles. No asignar participación estudiantil a los agentes: completar los nombres y aportes reales en el plan de trabajo.
