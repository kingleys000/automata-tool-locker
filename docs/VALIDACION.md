# Validación de la primera versión

Última revisión ejecutada: 18 de octubre de 2026.

## Comprobaciones ejecutadas

| Comprobación | Resultado |
|---|---|
| Suite pytest | **36 pruebas aprobadas**, sin omisiones en el entorno instalado |
| Configuración de cámara | El formulario utiliza el índice y la ROI configurados; al recargar conserva los de la sesión |
| Diez ciclos completos del motor | Aprobados con observaciones controladas dentro de los tests |
| Errores y recuperación | Herramienta incorrecta, baja confianza, imagen antigua, desconexión, sensor contradictorio, reinicio y reintento |
| Doble solicitud y concurrencia | Un solo préstamo; reenvíos idempotentes |
| Permisos | Escrituras remotas y origen/token inválidos rechazados; monitor sin token ni controles |
| Dataset | Capturas recientes, nombres seguros y rechazo de una sesión compartida entre conjuntos |
| Interfaz | Revisada con Edge en 1440×1000, 1280×800, 800×1280 y 390×844 |
| Vista de exposición | Ambos diagramas completos dentro de una tablet horizontal de 1280×800 |
| Reconexión | Aviso de datos desactualizados al cortar conexión; recuperación al restablecerla |
| Ciclo completo en navegador | Solicitud, retiro, devolución y aprobación desde los botones; segundo navegador de lectura sincronizado |
| Actualización observada en ese ciclo | **96 ms** entre solicitar y observar Reservada en el monitor, en la máquina local |
| Sintaxis JavaScript y compilación Python | Correctas |
| Dependencias | `pip check` sin conflictos; OpenCV y PyTorch importados correctamente |

La medida de 96 ms es una observación de una prueba local, no un percentil de rendimiento ni una medición sobre la red Wi-Fi de la feria.

La revisión del 18 de octubre ejecutó las pruebas de navegador contra el servidor aislado de `tests/browser_fixture.py`, incluyendo las capturas de pantalla. Las detecciones visibles en esas capturas son observaciones controladas de prueba. No representan un modelo entrenado ni una cámara conectada. No se modificó la base de préstamos del proyecto para esas pruebas.

`pytest.ini` limita la búsqueda a `tests/`. En el entorno restringido de Codex, Windows negó acceso a directorios temporales de pytest; la suite completa se ejecutó correctamente fuera de esa restricción.

## Entorno

Python 3.12.14; Flask 3.1.3; Waitress 3.0.2; OpenCV 4.14.0; Ultralytics 8.4.178; PyTorch 2.14.1 CPU. Las versiones completas están en `requirements-lock.txt`. Se utiliza Edge sin ventana para las pruebas de navegador.

## Evidencia generada

- `artifacts/monitor-exposicion.png`: diagramas en vista ampliada de tablet.
- `artifacts/monitor-tablet.png` y `monitor-portrait.png`: diseño adaptable.
- `artifacts/control-desktop.png` y `control-mobile.png`: interfaz de operación.
- `artifacts/browser-cycle.json`: resultado del ciclo de navegador y latencia observada.
- `tests/test_engine.py`, `test_web.py`, `test_camera_dataset.py`: pruebas reproducibles.

El servidor de `tests/browser_fixture.py` usa una base temporal y observaciones controladas únicamente para probar la interfaz. No abre una cámara, no entrena un modelo y no modifica `data/prestamos.sqlite`. No existe un endpoint de producción para inyectar resultados de reconocimiento.

## Pendiente de validación física

No se han conectado el Android ni una tablet física, y todavía no hay fotografías propias ni un modelo de herramientas entrenado. Por tanto, **no se ha medido exactitud de reconocimiento**, no se han completado los diez ciclos con cámara real y no se ha validado la red de la feria.

La instalación permite capturar imágenes y entrenar/evaluar el modelo siguiendo RECONOCIMIENTO.md. Hasta entonces el portal identifica la falta del modelo y bloquea las operaciones que necesitan evidencia visual. El verificador de dataset informa las clases faltantes y el evaluador informa la ausencia de `models/herramientas.pt`.

La caja, la puerta automática y sus sensores reales corresponden a la siguiente etapa y no se han construido ni probado.
