# Instrumentos para sustentar el proyecto

Estos formatos se diligencian durante las actividades reales. Los campos vacíos no constituyen resultados. Usar códigos de participante y evitar datos personales innecesarios.

## Ficha de observación del proceso

Fecha: ____  Lugar: ____  Observador: ____  Autorización del responsable: ____

| Paso observado | Actor por rol | Entrada | Registro utilizado | Resultado | Dificultad observada y evidencia |
|---|---|---|---|---|---|
| Solicitud | | | | | |
| Consulta de disponibilidad | | | | | |
| Entrega | | | | | |
| Devolución | | | | | |
| Revisión | | | | | |

Distinguir situaciones observadas de comentarios del participante y de interpretaciones del equipo. Registrar frecuencia solo si se midió, con período y número de observaciones.

## Entrevista al encargado

Participante por rol: ____ Fecha: ____ Registro autorizado: ____

1. ¿Cómo se solicita y autoriza hoy un préstamo?
2. ¿Dónde se registra la herramienta y su responsable?
3. ¿Cómo se consulta la disponibilidad?
4. ¿Cómo se comprueba una devolución y quién revisa el estado de la herramienta?
5. ¿Qué ocurre si hay pérdida, daño o desacuerdo sobre la devolución?
6. ¿Qué dificultades ha experimentado y qué registro permite documentarlas?
7. ¿Qué parte del prototipo sería útil y qué reglas deben ajustarse?

Guardar respuestas textuales autorizadas o paráfrasis identificadas. La entrevista sirve para validar requisitos; no es una encuesta estadísticamente representativa.

## Protocolo de evaluación visual

Documentar cámara, iluminación, fondo, región de interés, versiones, modelo y configuración. Separar conjuntos por sesión para evitar que imágenes casi idénticas aparezcan en entrenamiento y evaluación. Registrar conteos por clase y sesión. Usar `tools/train_model.py` y `tools/evaluate_model.py` de acuerdo con `docs/RECONOCIMIENTO.md`.

Conservar matriz de confusión, número total de muestras, errores por clase y falsos positivos de martillo. La confianza de clasificación no equivale a exactitud: un umbral 0,85 es un parámetro, no una precisión demostrada del 85 %. Los umbrales de aceptación finales deben acordarse antes de evaluar y justificarse en función del riesgo de aceptar un objeto incorrecto.

## Protocolo de diez ciclos

Precondiciones: modelo cargado, cámara activa, escena preparada, configuración registrada y herramienta disponible. Para cada ciclo realizar solicitud, retiro, cierre/verificación, devolución, cierre/verificación, revisión humana y aprobación. Registrar fechas, duración, resultado y eventos exportados. Ante un fallo conservar la evidencia y registrar el reintento por separado. No borrar intentos fallidos para completar una serie de diez éxitos.

Usar [registro_ciclos.csv](evidencias/registro_ciclos.csv). Resultado posible: no ejecutado, aprobado, fallido o interrumpido. Un ciclo solo se aprueba cuando termina disponible, no quedan préstamos activos y la secuencia de eventos corresponde con lo observado. Identificar siempre que puerta y sensor son simulados.

## Catálogo de evidencia

| Evidencia | Qué demuestra | Qué falta registrar |
|---|---|---|
| Suite automatizada | Reglas, permisos, persistencia y escenarios controlados | Comando, fecha, entorno y resultado |
| Capturas de interfaz | Pantallas y disposición de controles | Origen y condición simulada o real |
| Registro de observación | Procedimiento del laboratorio | Fecha, rol y autorización |
| Evaluación del modelo | Desempeño sobre el conjunto evaluado | Dataset, versión y matriz de confusión |
| CSV de eventos y ciclos | Secuencia y resultados de ejecución | Correlación entre ciclo e historial |

Las capturas existentes en `artifacts/` fueron producidas en pruebas de interfaz con observaciones controladas según `docs/VALIDACION.md`. Su presencia no demuestra que se entrenó un modelo propio.
