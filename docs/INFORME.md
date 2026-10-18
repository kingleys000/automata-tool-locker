# Sistema de préstamo de herramientas con autómatas y visión artificial

## Problema y objetivo

En un laboratorio se necesita conocer quién retira una herramienta, impedir préstamos simultáneos y verificar devoluciones. El prototipo administra una unidad de martillo e identifica visualmente herramientas pequeñas en una escena controlada. La maqueta física se incorpora después de validar esta etapa.

La cámara y el modelo generan observaciones, el controlador decide las transiciones y SQLite conserva los datos. El portal de la tablet representa el estado del servidor; no ejecuta un segundo autómata independiente.

## Modelo del inventario

Q = {Disponible, Reservada, Prestada, En revisión, Fuera de servicio}.

q₀ = Disponible. Este estado representa disponibilidad administrativa; la apertura requiere además presencia y reconocimiento válidos.

Σ = {solicitud_verificada, retiro_verificado, cancelacion_verificada, devolucion_verificada, aprobacion, dano, reparacion}.

| Estado | Evento | Siguiente |
|---|---|---|
| Disponible | solicitud_verificada | Reservada |
| Reservada | retiro_verificado | Prestada |
| Reservada | cancelacion_verificada | Disponible |
| Prestada | devolucion_verificada | En revisión |
| En revisión | aprobacion | Disponible |
| En revisión | dano | Fuera de servicio |
| Fuera de servicio | reparacion | En revisión |

La implementación usa una tabla determinista de transiciones. Las acciones de bajo nivel que no satisfacen las condiciones se rechazan, conservando el estado y emitiendo una salida de rechazo. Formalmente, el controlador puede representarse como una máquina de estados finitos con salidas y condiciones de entrada discretizadas. Los usuarios, tiempos y filas de préstamos son datos auxiliares; no constituyen estados infinitos del AFD académico.

Los identificadores e1, e2… del dibujo son abreviaturas locales de las filas de cada tabla, no símbolos compartidos entre los dos autómatas.

## AFD reconocedor y lenguaje regular

Para reconocer trazas se define M = (Q ∪ {Error}, Σ, δ, Disponible, {Disponible}). Se completa δ enviando cada par estado/símbolo no indicado a Error; desde Error, cualquier símbolo permanece en Error. Las secuencias válidas que terminan en Disponible son aceptadas. ε también se acepta porque el estado inicial es de aceptación.

Ejemplo aceptado: solicitud_verificada · retiro_verificado · devolucion_verificada · aprobacion.

Ejemplo aceptado: solicitud_verificada · cancelacion_verificada.

Ejemplo válido pero no aceptado como ciclo terminado: solicitud_verificada · retiro_verificado (termina en Prestada).

Ejemplo inválido: retiro_verificado desde Disponible, que conduce a Error.

Este reconocedor se encuentra en `app/automata.py`, función `recognize`. No debe confundirse con el controlador de interfaz: el reconocedor evalúa una traza completa; el controlador rechaza una acción individual y permite corregirla.

## Modelo de operación

Qop = {Inactiva, Abriendo, Esperando retiro, Esperando depósito, Cerrando, Verificando, Completada, Incidencia}.

El modo finito {préstamo, devolución, cancelación} determina qué observación se exige. Puede formalizarse mediante el producto del estado de operación y el modo, junto con entradas discretas de puerta, presencia y evidencia visual. Cada par estado/evento tiene como máximo un siguiente estado.

La ruta nominal es Inactiva → Abriendo → Esperando retiro o Esperando depósito → Cerrando → Verificando → Completada → Inactiva. Un fallo durante la operación conduce a Incidencia. El reintento retorna a Abriendo si la puerta está cerrada o a la espera correspondiente si sigue abierta. El inventario no se libera por un fallo.

Las tablas completas se generan en el portal desde la misma definición que consulta el motor. Los eventos de fallo/reinicio son entradas explícitas. La transición a Completada requiere evidencia capturada después del cierre, no una detección anterior.

## Arquitectura y consistencia

Python/Flask expone control y monitor; Waitress sirve el portal. Un hilo comparte la captura real, y un vigilante invalida evidencia antigua y tiempos agotados. Un bloqueo serializa las decisiones; las actualizaciones de estado, préstamos e historial se confirman en una transacción SQLite. Una restricción única impide dos préstamos activos del mismo martillo. Los identificadores de acción evitan repetir una operación tras un reenvío de red.

La tablet consulta cada 500 ms. El historial tiene secuencias crecientes y paginación; recuperar los eventos no causa nuevas transiciones. Las escrituras requieren conexión local, origen válido y token que no se entrega al monitor. No se necesita internet durante la operación una vez instalados software y modelo.

## Visión y límites experimentales

El modelo YOLO11n-cls se ajustará con cinco clases propias. Se conserva la herramienta completa al recortar y rellenar la región observada. La estabilidad combina umbral inicial 0,85, cinco observaciones como mínimo y duración mínima de dos segundos. La evidencia caduca a los 1,5 segundos sin observaciones recientes. Las puntuaciones no certifican exactitud ni identifican unidades iguales.

La revisión de daños es humana. Un sensor de presencia solo indica ocupación. En esta etapa sus lecturas y el cierre son simulados, por lo que la devolución queda registrada como verificación visual con hardware simulado, no como prueba de depósito físico.

## Evaluación pendiente de completar con datos reales

Las pruebas automatizadas verifican lógica, autorización, persistencia, eventos inválidos, fallos y diez ciclos con observaciones controladas. Sus resultados se describen en VALIDACION.md.

Tras capturar imágenes se deben añadir a este informe: número de imágenes por clase y sesión; configuración y duración del entrenamiento; matriz de confusión; falsos positivos; umbral final; latencia medida; resultados de diez ciclos con celular y evidencia exportada. No se asignan cifras de precisión hasta ejecutar esas mediciones.

## Fuentes técnicas

- Flask y Waitress: https://flask.palletsprojects.com/en/stable/deploying/waitress/
- YOLO11: https://docs.ultralytics.com/models/yolo11/
- Clasificación: https://docs.ultralytics.com/tasks/classify/
- Dataset: https://docs.ultralytics.com/datasets/classify/
- DroidCam: https://droidcam.app/help/
