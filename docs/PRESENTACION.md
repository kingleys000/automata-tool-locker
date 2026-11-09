---
marp: true
title: Sistema de préstamo de herramientas con autómatas y visión artificial
---

# Sistema de préstamo de herramientas con autómatas y visión artificial

**Autor(es):** [Nombre del autor / autores]

**Modalidad:** [Pasantía / Proyecto aplicado / Investigación]

**Semestre académico:** [2026-2]

---

# Tool lending system based on finite automata and computer vision

**Author(s):** [Author name(s)]

**Academic term:** [2026-2]

---

# Generalidades del proyecto

**Resumen:**
Se propone un sistema de préstamo de herramientas para un laboratorio, basado en dos autómatas finitos: uno administra el inventario (disponible, reservada, prestada, en revisión, fuera de servicio) y otro controla la operación física (apertura, retiro/depósito, cierre y verificación). Una cámara con un modelo de clasificación YOLO11n-cls verifica visualmente la herramienta antes de autorizar cada transición, y SQLite conserva préstamos e historial. El prototipo se valida con un martillo, puerta y sensores simulados, un portal web local y un monitor sincronizado en tablet.

**Palabras clave:** autómatas finitos, visión artificial, préstamo de herramientas, YOLO, sistemas embebidos, verificación visual.

**Abstract:**
We propose a tool-lending system for a laboratory, built on two finite automata: one manages the inventory (available, reserved, lent, under review, out of service) and the other controls the physical operation (opening, pick-up/return, closing and verification). A camera with a YOLO11n-cls classification model visually verifies the tool before authorizing each transition, while SQLite stores loans and history. The prototype is validated with one hammer, simulated door and sensors, a local web portal and a synchronized tablet monitor.

**Keywords:** finite automata, computer vision, tool lending, YOLO, embedded systems, visual verification.

---

# Research Problem

In a laboratory there is no reliable record of **who takes a tool**, simultaneous loans of the same unit are possible, and **returns are not verified**. Manual control depends on memory and trust, which leads to losses and unavailable tools. The research problem is: **how to guarantee that each loan and return is authorized, unique and visually verified**, using a deterministic control model (finite automata) combined with real-time computer vision, before investing in the physical cabinet hardware.

---

# Justificación

- **Técnica:** un autómata finito determinista elimina ambigüedad en las transiciones; cada evento inválido se rechaza y se registra, y la verificación visual exige evidencia nueva tras cada operación.
- **Práctica:** reduce pérdidas y préstamos simultáneos sin vigilancia permanente; la restricción única en SQLite impide dos préstamos activos del mismo martillo.
- **Académica:** aplica de forma medible la teoría de autómatas y lenguajes regulares (AFD reconocedor de trazas válidas) junto con visión artificial en un caso real.
- **Económica:** funciona con hardware de bajo costo (computador, celular como cámara) y sin internet una vez instalado; la maqueta física solo se construye tras validar el software.

---

# Marco Teórico o Conceptual

- **Autómatas finitos deterministas (AFD):** el inventario se modela como M = (Q, Σ, δ, q₀, F) con Q = {Disponible, Reservada, Prestada, En revisión, Fuera de servicio} y Σ = {solicitud_verificada, retiro_verificado, cancelacion_verificada, devolucion_verificada, aprobacion, dano, reparacion}.
- **Lenguajes regulares:** se define un AFD reconocedor con estado de Error; las trazas que terminan en Disponible son aceptadas, lo que permite validar ciclos completos de préstamo.
- **Máquinas de estados con salidas:** el controlador de operación (Inactiva → Abriendo → Esperando retiro/depósito → Cerrando → Verificando → Completada) actúa como transductor con entradas discretizadas de puerta, presencia y evidencia visual.
- **Visión artificial:** clasificación de imágenes con YOLO11n-cls ajustado a cinco clases propias (martillo, destornillador, alicate, vacío, otros), con estabilidad temporal (umbral 0,85, ≥ 5 observaciones, ≥ 2 s).

---

# Marco Contextual

- **Área de intervención:** laboratorio de herramientas de la institución [nombre de la institución], donde estudiantes y docentes retiran herramientas menores.
- **Descripción institucional:** el control actual es manual; no existe registro confiable de quién retira cada herramienta ni verificación de devoluciones.
- **Alcance del prototipo:** una unidad de martillo, escena controlada con cámara (celular por DroidCam o webcam V4L), computador local como servidor y tablet como monitor de solo lectura.
- **[Insertar mapa/localización del laboratorio y fotografía del contexto]**

---

# Marco Normativo

- **Normas generales aplicables:** [reglamento interno del laboratorio; políticas de préstamo de equipos de la institución].
- **Normas técnicas y sectoriales:** [RETIE si se incorpora electrónica de la puerta; NSR-10 si se construye la maqueta; buenas prácticas de seguridad eléctrica de baja tensión].
- **Tratamiento de datos:** las imágenes se capturan localmente, sin captura automática de rostros ni subida a servicios externos, conforme a principios de minimización de datos personales.
- **ODS relacionados:** ODS 4 (educación de calidad: laboratorios mejor gestionados), ODS 9 (industria, innovación e infraestructura), ODS 12 (producción y consumo responsables: menor pérdida de herramientas).

---

# Objetivos

**Objetivo general**

Diseñar e implementar un prototipo de sistema de préstamo de herramientas basado en autómatas finitos y visión artificial, que autorice, registre y verifique cada retiro y devolución en un laboratorio.

**Objetivos específicos**

1. Modelar el inventario y la operación física como autómatas finitos deterministas con trazas de validación.
2. Implementar el controlador, la persistencia en SQLite y el portal web con monitor sincronizado.
3. Construir un dataset propio de cinco clases y ajustar un modelo YOLO11n-cls con evaluación documentada.
4. Validar el sistema con diez ciclos completos de préstamo/devolución con cámara real.

---

# Metodología

**Fases metodológicas y productos**

| Fase | Actividades | Productos |
|---|---|---|
| 1. Modelado | Definir estados, alfabeto y transiciones; AFD reconocedor | Tablas de transición, `app/automata.py` |
| 2. Implementación | Motor, persistencia, portal, monitor, simulador | Software funcional + 47 pruebas aprobadas |
| 3. Visión | Captura de dataset (100 imágenes/clase), entrenamiento, evaluación | `models/herramientas.pt`, matriz de confusión |
| 4. Validación | Diez ciclos reales, métricas de latencia y exactitud | Informe de validación con datos reales |
| 5. Documentación | Informe técnico y presentación | Documento de trabajo de grado |

---

# Cronograma

| Actividad | M1 | M2 | M3 | M4 | M5 | M6 |
|---|---|---|---|---|---|---|
| Modelado de autómatas | █ | | | | | |
| Implementación del prototipo | █ | █ | | | | |
| Dataset y entrenamiento del modelo | | | █ | █ | | |
| Validación con ciclos reales | | | | █ | █ | |
| Redacción y sustentación | | | | | █ | █ |

*[Ajustar meses según el calendario académico]*

---

# Expected Results

- A working prototype that authorizes, records and verifies every loan and return, rejecting invalid events deterministically.
- A custom image dataset (five classes, ~100 images per class) and a fine-tuned YOLO11n-cls model with documented confusion matrix, accuracy and false positives.
- Measured results from ten complete loan/return cycles with the real camera, including latency and visual evidence.
- An academic validation of finite automata and regular languages applied to access control: accepted traces correspond to complete, correct lending cycles.
- A validated software base ready for the next milestone: the physical cabinet with real door and presence sensors.

---

# Bibliografía

1. Hopcroft, J. E., Motwani, R. y Ullman, J. D. (2007). *Introduction to Automata Theory, Languages, and Computation* (3.ª ed.). Pearson.
2. Sipser, M. (2013). *Introduction to the Theory of Computation* (3.ª ed.). Cengage Learning.
3. Redmon, J. y Farhadi, A. (2018). *YOLOv3: An Incremental Improvement*. arXiv:1804.02767.
4. Ultralytics (2024). *YOLO11 Documentation*. https://docs.ultralytics.com/models/yolo11/
5. Ultralytics (2024). *Image Classification Tasks*. https://docs.ultralytics.com/tasks/classify/
6. Ultralytics (2024). *Classification Datasets*. https://docs.ultralytics.com/datasets/classify/
7. Pallets Projects (2024). *Flask: Deploying with Waitress*. https://flask.palletsprojects.com/en/stable/deploying/waitress/
8. Jocher, G. et al. (2023). *Ultralytics YOLOv8*. Zenodo. https://doi.org/10.5281/zenodo.7347926
9. Dev47Apps (2024). *DroidCam User Guide*. https://droidcam.app/help/
10. Bradski, G. (2000). *The OpenCV Library*. Dr. Dobb's Journal of Software Tools.

*[Completar con citas institucionales y normativas según los lineamientos de la facultad]*
