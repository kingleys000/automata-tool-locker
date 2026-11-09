# Base común de los tres avances

## Título y propósito

Sistema de préstamo de herramientas basado en autómatas finitos y verificación visual.

El propósito es construir y estudiar un prototipo local que controle el ciclo de préstamo de una unidad de martillo, registre su responsable y exija las condiciones previstas antes de aceptar cada transición. El caso de aplicación es un laboratorio académico; la institución concreta y su procedimiento actual requieren confirmación del equipo.

## Pregunta del proyecto

¿Cómo representar y controlar el préstamo y la devolución de una herramienta mediante autómatas finitos, registro persistente y evidencia visual, dentro de un prototipo académico de alcance controlado?

## Objetivos

**General.** Desarrollar un prototipo local de préstamo de una herramienta que aplique autómatas finitos para controlar operaciones, conservar registros y verificar retiros y devoluciones con evidencia visual.

1. Modelar inventario y operación mediante estados, eventos y transiciones, y definir un reconocedor de trazas que permita explicar ciclos válidos e inválidos.
2. Implementar el motor, el almacenamiento SQLite y las interfaces de control y monitor, preservando la unicidad de préstamos activos y el rechazo de acciones inválidas.
3. Preparar un dataset propio de cinco clases, ajustar un clasificador y evaluar sus resultados con datos separados del entrenamiento.
4. Validar la lógica mediante pruebas automatizadas y completar diez ciclos documentados con cámara real y hardware simulado.

El simulador independiente constituye un recurso didáctico para explicar los objetivos 1 y 2. La caja física pertenece a una etapa posterior.

## Decisiones de alcance

| Decisión | Razón | Consecuencia para la sustentación |
|---|---|---|
| Una unidad de martillo | Permite delimitar estados y comprobar invariantes | No se presenta como inventario general de múltiples unidades |
| Dos máquinas de estados | La disponibilidad y la secuencia de operación tienen responsabilidades distintas | Explicar ambos diagramas y su coordinación |
| Clasificación de cinco clases | Distinguir martillo, destornillador, alicate, vacío y otros en una región controlada | No afirmar identificación de ejemplares iguales ni detección automática de daños |
| SQLite local | Persistir operaciones en un prototipo de un servidor | El simulador independiente mantiene datos de sesión en memoria |
| Códigos de demostración | Facilitar pruebas de roles y reglas | No afirmar autenticación robusta de usuarios reales |
| Puerta y presencia simuladas | Permitir validar lógica antes de construir mecanismo | La devolución registra verificación visual con hardware simulado |

## Estado de evidencia al 5 de noviembre de 2026

Se volvió a ejecutar la suite con `.venv/bin/python -m pytest -q --basetemp=/tmp/avances-pytest-20261105`: **47 pruebas aprobadas en 0,62 s**. Son pruebas automatizadas con observaciones controladas; no establecen exactitud del modelo ni resultados de laboratorio real. Las mediciones de navegador de octubre permanecen como antecedentes documentados, no se han repetido en esta revisión.

El código incorpora captura, entrenamiento y evaluación. La disponibilidad efectiva de un modelo propio y de una cámara conectada debe comprobarse antes de la demostración del módulo visual. No se asignan métricas de reconocimiento sin ejecutar esa evaluación.

## Información que debe aportar el equipo

| Dato | Cómo obtenerlo | Uso |
|---|---|---|
| Integrantes y asignación de roles | Acuerdo del equipo | Portadas, cronograma y participación |
| Institución y laboratorio | Confirmación del responsable | Contextualización del problema |
| Proceso actual y dificultades | Observación y entrevista con el instrumento adjunto | Sustento del análisis |
| Fechas de entrega | Cronograma de la asignatura | Convertir semanas relativas en fechas |
| Plantillas oficiales | Archivos proporcionados por la profesora | Montaje final Word y PowerPoint |

Estos pendientes no se resuelven inventando nombres, entrevistas o fechas. El contenido técnico y los instrumentos están listos para su revisión y diligenciamiento.
