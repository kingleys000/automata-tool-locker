# Plan de trabajo del proyecto

## 1. Propósito y punto de partida

Este plan convierte la metodología de `docs/AVANCE3_METODOLOGIA.md` en actividades asignables, secuenciadas y verificables. Atiende la organización del equipo solicitada por la [guía del Avance 3](https://avance3proyectoaula.netlify.app/), conservada en `docs/avances/fuentes/guia_avance3.md`, y sirve para cerrar el prototipo existente sin presentar como terminadas las validaciones que todavía requieren personas, dispositivos o evidencia institucional.

El punto de partida es el repositorio actual y la base común `docs/avances/BASE_PROYECTO.md`:

- Existen los dos autómatas y el AFD reconocedor en `app/automata.py`.
- Existen motor, persistencia SQLite, cámara, portal y monitor en `app/`, `templates/` y `static/`.
- Existe un simulador independiente en `simulator/`, con estado en memoria y cinco escenarios.
- Existen scripts para revisar dataset, entrenar y evaluar en `tools/`, y pruebas automatizadas en `tests/`.
- La base común registra una ejecución del 5 de noviembre de 2026 con **47 pruebas aprobadas en 0,62 s**; son pruebas automatizadas con observaciones controladas, no resultados de visión ni de laboratorio real.
- `docs/VALIDACION.md` y `docs/SIMULADOR.md` conservan antecedentes de software y navegador. Este plan no presenta ninguna de esas ejecuciones como propia ni como validación con cámara real.
- No se encuentran dataset propio ni `models/herramientas.pt` en el árbol consultado. La puerta y los sensores son simulados; no hay Arduino ni mecanismo físico implementado.
- El contexto del laboratorio debe validarse conforme a `docs/AVANCE4_ANALISIS.md`; no se presuponen observaciones ni entrevistas realizadas.

### Convención de estados

- **Disponible:** el producto técnico o documental existe, aunque todavía pueda requerir revisión o integración.
- **Pendiente humano:** exige asignación, autorización, juicio del equipo, captura, ejecución con dispositivos o revisión que no puede sustituirse por redacción.
- **Por ejecutar:** existe un procedimiento o una prueba, pero debe ejecutarse y registrarse sobre la versión que se entregará.
- **Bloqueado por dependencia:** no debe comenzarse hasta satisfacer la condición indicada.

“Disponible” no significa que un objetivo completo esté demostrado. Ninguna actividad pendiente debe marcarse como realizada sin una evidencia identificable.

## 2. Resultados que debe alcanzar el plan

El plan adopta el objetivo general y los cuatro objetivos específicos de la base común `docs/avances/BASE_PROYECTO.md`:

| ID | Resultado esperado | Condición verificable de avance |
|---|---|---|
| OE1 | Inventario y operación modelados mediante estados, eventos y transiciones, con reconocedor de trazas | Modelos revisados contra `app/automata.py`; ciclos válidos e inválidos y rechazos con pruebas asociadas |
| OE2 | Motor, SQLite e interfaces de control y monitor | Unicidad de préstamos activos, persistencia, idempotencia, permisos, rechazo de acciones inválidas y sincronización comprobados en la versión de entrega |
| OE3 | Dataset propio de cinco clases, clasificador ajustado y evaluación con datos separados | Dataset revisado por sesiones; modelo compatible; métricas y predicciones archivadas |
| OE4 | Lógica validada mediante pruebas automatizadas y diez ciclos documentados con cámara real y hardware simulado | Resultados de la versión de entrega, diez registros I-06 e historial exportado, con incidencias sin ocultar |

La parte de cámara real del OE4 sigue pendiente aunque `tests/test_engine.py` y `tests/test_simulator.py` contengan diez ciclos controlados. La meta de aproximadamente 100 imágenes por clase procede de `docs/RECONOCIMIENTO.md`; no constituye un conteo existente ni una garantía de exactitud.

## 3. Organización y asignación de responsables

### 3.1 Roles funcionales

Los siguientes roles describen responsabilidades, **no nombres ni participaciones ya acreditadas**. Una persona puede asumir más de un rol si el equipo lo acuerda, pero debe registrarse la asignación y mantener revisión cruzada siempre que sea posible.

| Rol | Responsabilidad principal | No puede darse por satisfecho sin |
|---|---|---|
| **RC — Coordinación académica** | Asignar personas, convertir semanas relativas a fechas oficiales, controlar dependencias, convocar revisiones y aprobar entregables | Acta o registro de acuerdos, calendario y revisión final |
| **RA — Análisis y modelado** | Validar contexto, actores, requisitos, estados, eventos y trazas | Evidencia de contexto y matriz de requisitos revisada |
| **RD — Desarrollo y arquitectura** | Conservar la reproducibilidad, revisar código, resolver defectos autorizados y preparar la ejecución local | Versión identificada, comandos y salidas reproducibles |
| **RV — Visión y datos** | Preparar escena, capturar clases, revisar etiquetas, entrenar y evaluar el modelo | Dataset real, metadatos, modelo y evaluación generada |
| **RQ — Calidad y validación** | Aplicar casos de prueba, registrar resultados, coordinar diez ciclos y analizar incidencias | Registros diligenciados, historial y evidencias de ejecución |
| **RR — Documentación y sustentación** | Integrar trazabilidad, anexos, presentación, límites y declaración de IA | Documento y presentación revisados contra las fuentes |

### 3.2 Asignación humana pendiente

RC debe completar esta tabla antes de iniciar la semana S1 del calendario oficial. No se proponen nombres ficticios.

| Rol | Persona asignada | Revisor o apoyo | Acuerdo pendiente |
|---|---|---|---|
| RC | Pendiente de asignación | Equipo | Disponibilidad, control del calendario y aprobación de cambios |
| RA | Pendiente de asignación | RC, RQ | Acceso al laboratorio y revisión de requisitos |
| RD | Pendiente de asignación | RQ | Versión de código y entorno de ejecución |
| RV | Pendiente de asignación | RQ, RD | Cámara, herramientas, captura, entrenamiento y custodia de datos |
| RQ | Pendiente de asignación | RA, RV | Protocolos, registros y análisis de fallos |
| RR | Pendiente de asignación | Todo el equipo | Plantillas oficiales, anexos y sustentación |

### 3.3 Reglas de trabajo

1. Cada tarea tiene un responsable principal; los apoyos revisan o suministran insumos, pero no diluyen la responsabilidad.
2. Toda ejecución registra entorno, versión/revisión, fecha real al ejecutarla, resultado y ruta de evidencia.
3. Un error se conserva en el registro; se corrige la causa y se repite el caso sin borrar el intento anterior.
4. Los cambios técnicos que afecten estados, reglas, clases o configuración exigen actualizar la trazabilidad y repetir las pruebas relacionadas.
5. Las cifras históricas se citan con su documento y alcance; no se copian como si correspondieran a otra versión, cámara o red.
6. La integración en documentos finales y plantillas oficiales corresponde al equipo/coordinación académica; este plan no presume que esa integración ya ocurrió.

## 4. Cronograma relativo

### 4.1 Referencia temporal

Se propone una secuencia de **diez semanas relativas (S1–S10)** para organizar el cierre y la consolidación. S1 comienza cuando el equipo asigne roles y confirme el calendario oficial; no es una fecha histórica ni una afirmación sobre cuándo se construyó el prototipo. RC debe sustituir las semanas por fechas reales sin alterar las dependencias. Las fases pueden solaparse, pero no se adelantan hitos que dependan de datos o dispositivos ausentes.

| Semana relativa | Fase metodológica | Actividad dominante | Hito de salida |
|---|---|---|---|
| S1 | 1. Análisis | Asignar roles; seleccionar contexto; observar proceso; revisar alcance | H1: contexto y requisitos con fuentes y pendientes explícitos |
| S2 | 2. Diseño | Revisar autómatas, arquitectura, datos, interfaces y matriz de pruebas | H2: diseño trazado a requisitos y casos |
| S3 | 3. Implementación | Confirmar entorno y versión; preparar cámara, escena y protocolo de captura | Condiciones listas para capturar sin autorizar préstamos reales aún |
| S4–S5 | 3. Implementación | Capturar y depurar dataset por clases y sesiones | Dataset completo y revisión I-04 |
| S6 | 3. Implementación y 4. Validación | Verificar estructura, entrenar, evaluar; repetir pruebas de software | H3: modelo y métricas reales, o limitación documentada si no se logra |
| S7–S8 | 4. Validación | Ejecutar diez ciclos reales, casos de incidencia y prueba de tablet/red | H4: resultados integrales, historial e incidencias |
| S9 | 4. Validación y 5. Documentación | Analizar resultados, aplicar ajustes autorizados y repetir pruebas afectadas | Resultados y límites cerrados para redacción |
| S10 | 5. Documentación | Integrar informe, anexos, presentación, declaración de IA y ensayo | H5: entrega revisada y demostración coherente con evidencias |

Si la captura o el entrenamiento se retrasa, S7–S10 se desplazan o el equipo informa el alcance realmente validado. No se sustituye el retraso con métricas inventadas ni con resultados del simulador.

### 4.2 Hitos y criterios de paso

| Hito | Responsable de verificar | Entradas obligatorias | Criterio de aceptación |
|---|---|---|---|
| H1. Análisis revisado | RC y RA | I-01, documentos autorizados si existen, RF/RNF | Proceso, actores y reglas identificados; supuestos no presentados como hechos |
| H2. Diseño trazable | RA y RD | Modelos, requisitos, arquitectura, I-02/I-03 | Cada requisito tiene componente, prueba y evidencia prevista |
| H3. Reconocimiento evaluable | RV y RQ | Dataset, revisión visual, modelo y evaluación | Cinco clases exactas; sesiones separadas; archivos de métricas generados desde ejecución real |
| H4. Operación integral registrada | RQ | Modelo válido, cámara, herramientas, guion, I-06 | Diez ciclos reales registrados; integridad revisada; fallos y recuperación explicados |
| H5. Entrega coherente | RC y RR | Trazabilidad, evidencias, documento y presentación | Objetivos con estado real; cifras respaldadas; límites y uso de IA declarados |

## 5. Actividades accionables

### 5.1 Fase 1 — Análisis del problema

| ID | Semana | Actividad y pasos | Responsable / apoyo | Evidencia y criterio de terminación | Estado inicial |
|---|---|---|---|---|---|
| A-01 | S1 | Asignar personas a RC, RA, RD, RV, RQ y RR; acordar revisiones y calendario | RC / equipo | Tabla 3.2 completa y calendario aprobado | Pendiente humano |
| A-02 | S1 | Identificar institución y laboratorio; gestionar acceso/autorización; definir qué evidencia puede conservarse | RA / RC | Contexto identificado y autorización o restricción registrada | Pendiente humano |
| A-03 | S1 | Aplicar I-01 a solicitud, entrega, devolución y revisión; contrastar actores, registros y excepciones | RA / RQ | Guion diligenciado y fuentes anexadas; sin inferencias no observadas | Pendiente humano |
| A-04 | S1 | Revisar RF01–RF10 y RNF01–RNF07; registrar diferencias entre contexto y prototipo | RA / RQ | Requisitos aceptados, modificados o marcados como propuesta | Pendiente humano |
| A-05 | S1 | Confirmar alcance de un martillo, hardware simulado y ausencia de autenticación productiva | RA / RD | Alcance sin contradicciones con README e informe | Base disponible; revisión pendiente |

### 5.2 Fase 2 — Diseño de la solución

| ID | Semana | Actividad y pasos | Responsable / apoyo | Evidencia y criterio de terminación | Estado inicial |
|---|---|---|---|---|---|
| D-01 | S2 | Comparar estados, eventos y transiciones de `docs/INFORME.md` con `app/automata.py`; revisar rutas nominal, cancelación, daño y recuperación | RA / RD | Tablas concordantes y discrepancias resueltas o anotadas | Disponible; revisión humana pendiente |
| D-02 | S2 | Revisar el AFD reconocedor y ejemplos de trazas; diferenciar aceptación de una traza y rechazo interactivo | RA / RQ | Casos aceptados, no aceptados e inválidos incluidos en I-03 | Disponible; consolidación pendiente |
| D-03 | S2 | Contrastar arquitectura, tablas y vistas con `app/web.py`, `app/engine.py`, `templates/` y `static/` | RD / RA | Diagramas y descripciones sin componentes inexistentes | Disponible; revisión humana pendiente |
| D-04 | S2 | Completar I-02 con RF/RNF, OE, componente, caso y evidencia prevista | RQ / RA | No hay requisito sin prueba ni prueba sin propósito | Pendiente humano |

### 5.3 Fase 3 — Implementación y construcción del reconocimiento

| ID | Semana | Actividad y pasos | Responsable / apoyo | Evidencia y criterio de terminación | Estado inicial |
|---|---|---|---|---|---|
| I-01 | S3 | Identificar la versión de entrega, recrear/confirmar entorno según README y registrar dependencias | RD / RQ | Comandos, versión y entorno documentados; base de datos real protegida durante pruebas | Por ejecutar |
| I-02 | S3 | Revisar que motor, portal, monitor, simulador y scripts correspondan al diseño; no ampliar alcance sin acuerdo | RD / RA | Lista de módulos y rutas verificada | Disponible; comprobación pendiente |
| I-03 | S3 | Seleccionar cámara, fijar escena, configurar ROI y registrar condiciones; evitar rostros y datos ajenos | RV / RD | Video real y encuadre revisados; configuración anotada | Pendiente humano |
| I-04 | S4–S5 | Capturar `martillo`, `destornillador`, `alicate`, `vacio` y `otros`; separar sesiones `train`, `val`, `test`; variar condiciones sin introducir pistas | RV / RQ | Archivos en `dataset/`, `dataset/sessions.json` y conteos reales por sesión | Pendiente humano |
| I-05 | S5 | Revisar etiquetas, duplicados, casi duplicados, oclusiones y legibilidad; corregir mediante recaptura cuando proceda | RV / RQ | I-04 completo y revisión visual firmada por rol | Pendiente humano |
| I-06 | S6 | Ejecutar comprobación estructural; si pasa, entrenar sin sustituir datos propios; conservar salida y metadatos | RV / RD | `models/herramientas.pt` y `models/entrenamiento.json` producidos por ejecución real | Bloqueado por I-04/I-05 |
| I-07 | S6 | Ejecutar evaluación sobre `test`; analizar matriz, exactitud y falsos positivos; no ajustar repetidamente con `test` | RV / RQ | `artifacts/evaluacion_modelo.json`, `artifacts/predicciones.csv` e interpretación con límites | Bloqueado por I-06 |

**Procedimiento de I-03 a I-07.** Seguir `docs/RECONOCIMIENTO.md`. Como referencia, en Linux:

```bash
.venv/bin/python tools/train_model.py --check
.venv/bin/python tools/train_model.py --epochs 40 --device cpu
.venv/bin/python tools/evaluate_model.py
```

El segundo comando solo se ejecuta si la estructura y la revisión visual son aceptables. El número de épocas mostrado es la configuración existente del procedimiento, no una ejecución reportada por este plan. Si el equipo cambia parámetros, registra el cambio y su justificación antes de evaluar.

### 5.4 Fase 4 — Pruebas y validación

| ID | Semana | Actividad y pasos | Responsable / apoyo | Evidencia y criterio de terminación | Estado inicial |
|---|---|---|---|---|---|
| V-01 | S6 | Ejecutar suite pytest y sintaxis JavaScript sobre la versión de entrega; guardar salida y entorno | RQ / RD | Resultado real por comando, sin convertir pruebas controladas en cámara real | Por ejecutar |
| V-02 | S6 | Ejecutar ciclos de navegador y simulador; revisar monitor, reconexión y diseños; conservar capturas de la ejecución | RQ / RD | Salidas y capturas asociadas a la versión | Por ejecutar |
| V-03 | S7–S8 | Ejecutar diez ciclos completos con cámara real; diligenciar I-06 por ciclo y exportar historial | RQ / RV | Diez registros, CSV, integridad de préstamos/devoluciones y estado final coherente | Bloqueado por H3 |
| V-04 | S8 | Ejecutar por separado objeto incorrecto, retiro anticipado, evidencia insuficiente, desconexión, sensor contradictorio, daño y reparación | RQ / RV | Resultado esperado/obtenido e incidencia/recuperación por caso | Bloqueado por H3 |
| V-05 | S8 | Conectar la tablet física a la red prevista; comprobar lectura, sincronización, aviso de desactualización y recuperación | RQ / RD | Registro con dispositivo/red reales; ausencia de controles de escritura | Pendiente humano |
| V-06 | S8–S9 | Calcular conteos y medidas descriptivas desde I-06; clasificar fallos y diferenciar imagen, estabilidad, red y regla | RQ / RV | Resumen con denominadores y método; todos los intentos conservados | Bloqueado por V-03/V-04 |
| V-07 | S9 | Aplicar solo ajustes acordados; repetir casos afectados y documentar cualquier limitación no resuelta | RD, RV / RQ | Cambio, causa, prueba repetida y nueva evidencia | Bloqueado por análisis previo |

**Procedimiento de V-01/V-02.** Los comandos de referencia son:

```bash
.venv/bin/python -m pytest -q --basetemp=.pytest_tmp
node --check static/app.js
node tests/browser_cycle.cjs
node tests/simulator_browser.cjs
```

Las pruebas de navegador usan servidores temporales y observaciones controladas según `README.md` y `docs/VALIDACION.md`. RQ debe comprobar que no se modifique `data/prestamos.sqlite` durante esas pruebas. La medida histórica de 96 ms pertenece a una ejecución local documentada y no es una meta ni un resultado de la tablet física.

**Procedimiento de V-03.** Para cada ciclo: preparar escena y modelo; seguir los pasos de préstamo, devolución y aprobación de `docs/DEMOSTRACION.md`; registrar tiempos solo si se miden; verificar responsable, préstamo único, evidencia posterior al cierre, devolución y aprobación; exportar/conservar el historial sin borrar incidencias. Los diez ciclos son ejecuciones con cámara real, no diez repeticiones del simulador.

### 5.5 Fase 5 — Documentación y presentación

| ID | Semana | Actividad y pasos | Responsable / apoyo | Evidencia y criterio de terminación | Estado inicial |
|---|---|---|---|---|---|
| C-01 | S9–S10 | Integrar metodología, plan, análisis, diseño, resultados y límites en las plantillas oficiales | RR / RC | Documento final con terminología y cifras concordantes | Base documental disponible; integración humana pendiente |
| C-02 | S9–S10 | Actualizar matrices OE/RF/RNF con resultados y rutas reales; separar implementado, ejecutado y propuesto | RR / RQ | Cada afirmación tiene fuente y cada pendiente conserva su estado | Pendiente humano |
| C-03 | S10 | Seleccionar diagramas, capturas, métricas, CSV e incidencias; rotular procedencia y alcance | RR / RQ, RV | Anexos legibles y referenciados desde el texto | Pendiente humano |
| C-04 | S10 | Preparar presentación y demostración; si falta modelo, limitar la demostración al simulador y declarar el pendiente | RR / RD, RQ | Guion viable con los recursos efectivamente disponibles | Pendiente humano |
| C-05 | S10 | Aplicar I-07; revisar aportes, declaración de IA, formato, referencias y ausencia de marcadores | RC / todo el equipo | Revisión final registrada y aprobación del equipo | Pendiente humano |

## 6. Matriz de evidencias y custodia

| Evidencia | Origen | Responsable | Ubicación existente o prevista | Regla de uso |
|---|---|---|---|---|
| Contexto y proceso actual | I-01 y documentos autorizados | RA | Anexo definido por el equipo | No afirmar campo sin aplicación y respaldo |
| Requisitos y trazabilidad | I-02 | RA, RQ | Documento/anexo oficial | Mantener enlace con componentes y casos |
| Modelos formales | Código e informe | RA | `app/automata.py`, `docs/INFORME.md` | Conservar nombres de estados/eventos |
| Pruebas de software | Pytest, Playwright, I-03 | RQ | `tests/`, salidas y capturas de la ejecución | Identificar versión, entorno y observaciones controladas |
| Dataset y separación | Capturas reales e I-04 | RV | `dataset/`, `dataset/sessions.json` | No mezclar sesiones ni añadir imágenes ficticias |
| Entrenamiento | Script y salida real | RV | `models/herramientas.pt`, `models/entrenamiento.json`, salida de entrenamiento | No afirmar que existe hasta comprobar el archivo |
| Evaluación visual | Script sobre `test` | RV, RQ | `artifacts/evaluacion_modelo.json`, `artifacts/predicciones.csv` | Reportar valores generados; no prellenar métricas |
| Ciclos reales | I-06 e historial | RQ | Registro del equipo y CSV exportado | Incluir fallos; separar de pruebas automatizadas |
| Interfaces | Capturas de control, monitor y simulador | RQ, RR | `artifacts/` y anexos seleccionados | Las capturas no prueban hardware físico ni exactitud |
| Documento y presentación | Integración académica | RR, RC | Plantillas oficiales | Revisar cifras, límites, IA y formato antes de entregar |

Las rutas “previstas” no implican que los archivos existan. Se conservarán los datos originales y, cuando se requieran copias de trabajo para análisis, se identificarán sin sobrescribir la evidencia. La base `data/prestamos.sqlite` no se utilizará como base desechable de pruebas; cualquier respaldo se hará con el servidor detenido, como indica `README.md`.

## 7. Dependencias, riesgos y decisiones

| Riesgo o dependencia | Señal verificable | Respuesta prevista | Responsable |
|---|---|---|---|
| Contexto no validado | No hay I-01 ni fuentes institucionales | Mantener el contexto como pendiente; gestionar acceso; no inventar hallazgos | RA, RC |
| Cámara o red no disponible | No abre video o la tablet no sincroniza | Registrar condición, revisar índice/permisos/red y reprogramar validación real | RD, RQ |
| Dataset insuficiente o contaminado | Faltan clases, sesiones mezcladas, duplicados o etiquetas incorrectas | No entrenar para “cerrar” el hito; corregir captura y revisión | RV |
| Modelo ausente o incompatible | Falta archivo o las clases no coinciden | Conservar bloqueo de préstamos; revisar entrenamiento/modelo | RV, RD |
| Falsos positivos o inestabilidad | Errores en matriz o imposibilidad de estabilizar | Analizar datos/escena; ajustar con `val`; reservar `test`; repetir evaluación | RV, RQ |
| Cambios de cámara, ROI o escena | Configuración diferente a la capturada | Capturar nuevas sesiones y repetir validación pertinente | RV |
| Confusión entre simulación y realidad | Resultados sin fuente de cámara/dispositivo | Etiquetar evidencia y corregir documento/presentación | RQ, RR |
| Pérdida o exposición de datos | Base usada en pruebas o imágenes con datos personales | Aislar pruebas, proteger respaldos y excluir/tratar datos conforme a autorización | RD, RV |
| Alcance físico no implementado | Se solicita demostrar puerta/Arduino como existente | Declarar etapa posterior; no simular una validación física | RC, RD |

**Decisiones que solo puede tomar el equipo:** aceptación del contexto y requisitos; asignación de personas y fechas; autorización de datos; criterio cuantitativo de aceptación del modelo antes de la evaluación final; correcciones de código; inclusión de hardware futuro; y alcance de la demostración si persisten pendientes.

## 8. Pendientes humanos precisos antes de cerrar el proyecto

1. **RC:** escribir los nombres reales en la tabla 3.2, acordar revisiones y convertir S1–S10 a fechas del calendario oficial.
2. **RA:** identificar institución/laboratorio y aplicar I-01 o registrar por qué no fue posible; validar actores, proceso y reglas.
3. **RA/RQ:** revisar RF01–RF10 y RNF01–RNF07, y completar I-02 con pruebas y evidencias.
4. **RD:** identificar la versión de entrega y confirmar instalación/ejecución sin usar la base real como ambiente de pruebas.
5. **RV:** conseguir y configurar cámara y herramientas; capturar las cinco clases con sesiones independientes; revisar manualmente el dataset.
6. **RV/RD:** ejecutar entrenamiento real y comprobar que el modelo contiene exactamente las cinco clases; conservar metadatos.
7. **RV/RQ:** ejecutar evaluación real sobre `test`, archivar JSON/CSV y redactar análisis sin prometer una exactitud previa.
8. **RQ:** repetir las pruebas de software y navegador sobre la versión final y guardar las salidas de esa ejecución.
9. **RQ/RV:** realizar diez ciclos de préstamo/devolución con cámara real, diligenciar I-06 y exportar el historial; registrar todos los fallos.
10. **RQ/RD:** probar tablet física, red local, sincronización, desconexión y recuperación en las condiciones previstas para la exposición.
11. **Equipo:** decidir, antes de la evaluación final, cualquier umbral de aceptación del modelo y justificarlo; el umbral de confianza 0,85 de `config.json` no equivale a exactitud del sistema.
12. **RR/RC:** integrar resultados reales en documentos y presentación finales, eliminar marcadores, revisar límites y aprobar la declaración de IA según la institución.
13. **Equipo:** si se decide construir la caja física, formular una etapa nueva con adaptador real, riesgos eléctricos/mecánicos y validación adicional; no incluirla como logro del prototipo actual.

## 9. Definición de terminado

El plan puede marcarse como completado únicamente cuando:

- Los roles tienen personas asignadas y las actividades tienen fechas reales y evidencias.
- H1 y H2 están aprobados con fuentes y trazabilidad revisadas.
- El software de entrega tiene resultados de pruebas propios de esa versión.
- El dataset, modelo y evaluación existen como archivos reales y fueron revisados, o el equipo declara expresamente que OE3 queda pendiente.
- Los diez ciclos reales y los casos de incidencia están registrados, o el equipo declara expresamente que OE4 queda pendiente.
- La tablet/red se prueba en condiciones reales o la limitación queda visible.
- Documento, presentación y demostración distinguen lógica, simulación, cámara real y hardware futuro.
- La revisión I-07 y la declaración de IA fueron verificadas por el equipo.

Si alguna condición no se cumple, el entregable debe informar el estado alcanzado y el pendiente; no se redefine “terminado” para ocultar la ausencia de evidencia.

## 10. Declaración de IA aplicada a este plan

Este plan se organizó con apoyo de **Kimi Code CLI** a partir de la guía del Avance 3, los objetivos existentes y la revisión del repositorio. La IA no asignó personas, no aplicó instrumentos de campo y no generó datos, entrenamientos, métricas ni ciclos reales. Las semanas S1–S10 y los roles funcionales son una propuesta de planificación que el equipo debe aprobar; las actividades pendientes solo podrán marcarse como realizadas cuando existan evidencias humanas y técnicas verificables. La declaración general y sus límites se complementan con la sección 8 de `docs/AVANCE3_METODOLOGIA.md`.
