# Guion de exposición — Avances 3, 4 y 5

**Presentación:** `docs/SUSTENTACION_AVANCES_JUAN_DIEGO.pptx`  
**Expositor:** Juan Diego Torres Molina  
**Duración estimada:** 12 a 14 minutos, más preguntas.

## Idea central

> El proyecto no consiste únicamente en reconocer una herramienta con una cámara. Consiste en controlar el ciclo completo de préstamo mediante reglas formales, evidencia visual y registros persistentes.

## Recomendaciones rápidas

- Usa estos apuntes como guía; evita leerlos literalmente.
- Presenta primero la necesidad y después la tecnología.
- Cuando muestres una cifra, explica también qué demuestra y qué no demuestra.
- Repite claramente que la puerta y los sensores están simulados y que el modelo propio de visión está pendiente.
- Si necesitas reducir el tiempo, resume las diapositivas 2, 4 y 10.

---

## 1. Portada — 40 segundos

### Qué decir

> Buenos días. Soy Juan Diego Torres Molina y presentaré los avances 3, 4 y 5 del proyecto “Sistema de préstamo de herramientas con autómatas finitos y verificación visual”.
>
> El propósito es controlar el préstamo y la devolución de una unidad de martillo en un escenario académico. Para lograrlo, el prototipo combina autómatas finitos, evidencia visual, almacenamiento SQLite e interfaces locales.
>
> Durante la exposición explicaré cómo se planteó el trabajo, qué necesidades y reglas se identificaron, cómo se diseñó la solución y qué resultados están efectivamente respaldados.

### Transición

> “Primero mostraré cómo se relacionan los tres avances”.

---

## 2. Tres avances, una sola historia — 45 segundos

### Qué decir

> Los tres avances responden preguntas diferentes, pero forman una misma cadena.
>
> El Avance 3, Metodología, explica cómo se construye y cómo se valida el proyecto. Define el enfoque, las fases, los instrumentos y los criterios de evidencia.
>
> El Avance 4, Análisis, establece qué debe controlar el sistema. Allí se identifican actores, requisitos, procesos y excepciones.
>
> El Avance 5, Diseño, muestra cómo se materializa ese análisis mediante arquitectura, autómatas, datos e interfaces.
>
> En síntesis: el análisis define las reglas, el diseño las representa y la metodología determina cómo comprobarlas.

### Frase para destacar

> “No son tres entregas aisladas: cada avance da soporte al siguiente”.

---

## 3. Avance 3 · Metodología — 1 minuto

### Qué decir

> El proyecto adopta un enfoque de investigación aplicada, iterativo y con evaluación experimental. Es aplicado porque aborda una necesidad concreta e iterativo porque una prueba puede llevar a corregir una regla, una interfaz o un procedimiento.
>
> La primera fase es analizar: delimitar actores, alcance y requisitos verificables.
>
> La segunda es diseñar: representar las reglas mediante autómatas y establecer una única autoridad de estado.
>
> La tercera es construir: implementar el motor, SQLite, el portal, el monitor y el simulador.
>
> La cuarta es validar, separando las pruebas de software, la evaluación visual y la operación con dispositivos reales.
>
> La quinta es comunicar: conservar la trazabilidad entre objetivos, componentes, pruebas, resultados y límites.

### Idea de cierre

> “El principio metodológico principal es que cada afirmación debe tener una evidencia identificable”.

---

## 4. La disciplina de la evidencia — 55 segundos

### Qué decir

> Para evitar afirmaciones mayores que las pruebas disponibles, el proyecto distingue tres estados.
>
> Implementado significa que existe código, documentación o evidencia identificable. En esa categoría están los autómatas, el motor, SQLite, las interfaces y el simulador.
>
> Documentado significa que una ejecución quedó registrada con su alcance. Por ejemplo, las pruebas automatizadas aprobadas con observaciones controladas.
>
> Pendiente significa que todavía se requiere trabajo de campo, cámara, herramientas o dispositivos reales. Aquí están el dataset propio, el modelo entrenado y los diez ciclos reales.
>
> Esta separación es importante porque tener un script de entrenamiento no equivale a tener un modelo entrenado, y ejecutar una simulación no equivale a validar una custodia física.

### Transición

> “Con este criterio de evidencia, el Avance 4 define qué debe cumplir el sistema”.

---

## 5. Avance 4 · Actores y necesidades — 1 minuto

### Qué decir

> El análisis identifica actores humanos y técnicos.
>
> El usuario solicita, retira y devuelve. El encargado inspecciona la herramienta y decide si la aprueba, reporta un daño o registra una reparación. El operador local configura el computador, la cámara y la región de interés.
>
> La visión artificial aporta observaciones y el adaptador de puerta y sensores reporta señales. Estos actores técnicos no deciden por sí solos si una operación es válida.
>
> Las necesidades se resumen en cuatro puntos. Primero, evitar dos préstamos activos de la misma unidad. Segundo, conservar un responsable verificable. Tercero, rechazar acciones inválidas sin modificar el estado y dejar auditoría. Cuarto, exigir revisión humana antes de que una herramienta devuelta vuelva a estar disponible.
>
> Estas necesidades se concretan en diez requisitos funcionales y siete no funcionales. El procedimiento concreto de una institución todavía debe confirmarse mediante trabajo de campo.

### Aclaración opcional

> Los códigos `1001`, `1002` y `ADMIN` son datos demostrativos, no un sistema institucional de autenticación.

---

## 6. Préstamo, devolución y revisión — 1 minuto 20 segundos

### Qué decir

> El ciclo comienza en Disponible. Para reservar, el usuario debe ser válido y el sistema debe contar con evidencia reciente y estable del martillo.
>
> Después de la reserva se coordina la apertura y el retiro. Sin embargo, el préstamo no se registra inmediatamente: primero debe confirmarse el cierre y debe existir evidencia visual posterior al cierre de que la casilla quedó vacía. Solo entonces el inventario pasa a Prestada.
>
> Para la devolución, el código debe corresponder al responsable del préstamo activo. Después del depósito y del cierre, se exige evidencia nueva de que el martillo está presente.
>
> La devolución cierra el préstamo, pero el inventario pasa a En revisión. El encargado puede aprobarlo para regresar a Disponible, registrar un daño para pasar a Fuera de servicio o certificar una reparación, que exige una nueva revisión.
>
> Si aparece un objeto incorrecto, se pierde una señal o se agota el tiempo de verificación, la operación entra en Incidencia y el inventario no se libera erróneamente.

### Aclaración necesaria

> “En esta etapa, la puerta y el sensor de presencia están simulados. El flujo demuestra la lógica, no una operación electromecánica real”.

---

## 7. Avance 5 · Dos autómatas coordinados — 1 minuto 20 segundos

### Qué decir

> El diseño utiliza dos autómatas porque existen dos responsabilidades diferentes.
>
> El autómata de inventario representa la condición administrativa del martillo: Disponible, Reservada, Prestada, En revisión o Fuera de servicio. Tiene cinco estados y siete eventos.
>
> El autómata de operación coordina la secuencia física: Inactiva, Abriendo, Esperando retiro, Esperando depósito, Cerrando, Verificando, Completada e Incidencia.
>
> Por ejemplo, que la herramienta esté prestada describe su condición administrativa, mientras que Cerrando describe una acción en curso. Mezclar ambos conceptos haría el modelo más difícil de verificar.
>
> Los autómatas son deterministas: para cada estado y evento definido existe como máximo un estado siguiente. Una acción no admitida se rechaza sin cambiar el estado actual.
>
> Además, el reconocedor de trazas incorpora un estado Error absorbente y acepta las secuencias válidas que terminan en Disponible.

### Frase para recordar

> “Inventario indica cómo está la herramienta; operación indica qué está ocurriendo”.

---

## 8. Arquitectura desacoplada y local — 1 minuto 5 segundos

### Qué decir

> La arquitectura separa interfaces, servicios, reglas, dispositivos y persistencia.
>
> El Centro de Control local puede enviar acciones, pero las mutaciones exigen dirección loopback, origen válido y token. El monitor solamente consulta y no recibe privilegios de escritura.
>
> Flask y Waitress exponen la API. El motor concentra las reglas y los autómatas, gestiona la concurrencia, la idempotencia y la verificación temporal.
>
> La cámara entrega observaciones y el adaptador simulado reporta puerta y presencia. El motor no supone que una orden física ya se ejecutó: espera la confirmación correspondiente.
>
> SQLite conserva estado, préstamos y auditoría mediante transacciones. El sistema funciona localmente, sin internet.
>
> Finalmente, el simulador utiliza el puerto 8001 y memoria RAM, mientras el prototipo principal utiliza el puerto 8000 y SQLite. El simulador no modifica los préstamos almacenados.

### Idea de cierre

> “Esta separación permite cambiar posteriormente el adaptador simulado sin trasladar las reglas de negocio a la cámara o a la interfaz”.

---

## 9. Verificación visual con límites explícitos — 1 minuto 5 segundos

### Qué decir

> La cámara observa, pero el motor decide. Una predicción aislada no autoriza una operación.
>
> La solución contempla cinco clases: martillo, destornillador, alicate, vacío y otros. El clasificador reconoce apariencia de categorías; no identifica una unidad específica ni determina automáticamente si una herramienta está dañada.
>
> La configuración actual exige confianza mínima de 0,85, estabilidad durante al menos dos segundos, cinco cuadros consecutivos con la misma etiqueta y observaciones con una frescura máxima de 1,5 segundos.
>
> Después del cierre se requieren observaciones nuevas. Si no existe evidencia concluyente dentro de los doce segundos configurados, se produce una incidencia y se habilita el reintento.
>
> Estos valores son parámetros configurables, no métricas de exactitud. El dataset propio y el modelo entrenado permanecen pendientes, por lo que el sistema bloquea las operaciones que exigen evidencia visual cuando no existe un modelo válido.

### Frase útil

> “Un umbral de confianza de 0,85 no significa que el modelo tenga 85 por ciento de exactitud”.

---

## 10. Datos e interfaces que hacen cumplir las reglas — 1 minuto

### Qué decir

> El diseño de datos utiliza cinco tablas: `users` para roles demostrativos, `loans` para préstamos, `events` para auditoría, `state` para el estado global y `requests` para idempotencia.
>
> La restricción principal es que `returned_at` nulo representa un préstamo activo. Un índice único parcial impide que la misma herramienta tenga dos préstamos activos, incluso como defensa adicional ante condiciones de carrera.
>
> La tabla `requests` evita que una petición retransmitida ejecute dos veces una acción. La tabla `events` conserva aceptaciones y rechazos con estados, origen y mensaje.
>
> En las interfaces, el Centro de Control permite acciones locales según el estado y el rol. El monitor presenta los autómatas y la conexión, pero no incluye token ni controles de escritura. Su consulta periódica está configurada cada 500 milisegundos, lo cual no equivale a garantizar una latencia máxima de red.

### Transición

> “Con esta base implementada, es importante precisar qué resultados ya están respaldados”.

---

## 11. Resultados actuales y ruta de validación — 1 minuto 10 segundos

### Qué decir

> La ejecución documentada del 5 de noviembre de 2026 registra 47 pruebas automatizadas aprobadas en 0,62 segundos. Estas pruebas cubren aspectos de lógica, persistencia, permisos, recuperación y simulador mediante observaciones controladas.
>
> No representan exactitud del reconocimiento, pruebas de una cerradura física ni validación completa en un laboratorio real.
>
> Para continuar, la primera tarea es validar el contexto institucional y el proceso real. La segunda es capturar el dataset propio por sesiones, manteniendo separados entrenamiento, validación y prueba.
>
> La tercera es entrenar y evaluar el modelo con datos independientes, conservando matriz de confusión, exactitud, falsos positivos y estabilidad temporal.
>
> La cuarta es ejecutar diez ciclos completos con cámara real, registrar también los fallos y probar la tablet en la red de exposición.
>
> El hardware físico y Arduino pertenecen a una fase posterior y requerirán diseño y validación adicionales.

### Idea de cierre

> “El proyecto presenta sus límites como parte del diseño y de la validación, no como información que deba ocultarse”.

---

## 12. Cierre y preguntas — 35 segundos

### Qué decir

> Como conclusión, el proyecto integra tres elementos: autómatas que determinan qué operaciones son válidas, evidencia visual que habilita determinadas transiciones y datos que permiten reconstruir lo ocurrido.
>
> El Avance 3 establece cómo construir y comprobar; el Avance 4 define qué controlar; y el Avance 5 explica cómo se diseñó la solución.
>
> El resultado es un prototipo académico con la lógica y la persistencia implementadas, con un alcance controlado y con una ruta concreta para completar la validación visual y física.
>
> Muchas gracias. Quedo atento a sus preguntas.

---

# Respuestas para preguntas probables

## ¿Por qué usar autómatas finitos?

Porque el préstamo tiene estados y eventos discretos que pueden formalizarse. El autómata define explícitamente qué acciones son válidas, facilita el rechazo de secuencias incorrectas y permite diseñar pruebas de ciclos válidos e inválidos.

## ¿Por qué utilizar dos autómatas?

Porque la disponibilidad administrativa y la operación física tienen responsabilidades distintas. Separarlas evita mezclar el estado del préstamo con acciones como abrir, cerrar o verificar.

## ¿La cámara puede autorizar un préstamo por sí sola?

No. La cámara entrega observaciones. El motor también valida estado, titularidad, puerta, presencia, frescura y estabilidad temporal antes de aceptar una operación.

## ¿Qué demuestran las 47 pruebas?

Demuestran el comportamiento de los casos automatizados evaluados con observaciones controladas. No son 47 pruebas físicas ni una medición de exactitud del modelo.

## ¿Por qué no se presenta una exactitud del reconocimiento?

Porque todavía no existe un dataset propio y un modelo entrenado que permitan calcularla. La evaluación debe ejecutarse con un conjunto de prueba independiente antes de reportar cualquier cifra.

## ¿Qué sucede si se devuelve un objeto diferente?

La operación entra en Incidencia, el préstamo permanece activo y el inventario no vuelve a Disponible. El caso debe corregirse y reintentarse, conservando la trazabilidad.

## ¿La devolución deja disponible inmediatamente el martillo?

No. La devolución cierra el préstamo y cambia el inventario a En revisión. Solo el encargado puede aprobar su regreso a Disponible después de inspeccionarlo.

## ¿El sistema ya controla una puerta física?

No. Actualmente utiliza `SimulatedHardware` para puerta y presencia. La integración con Arduino y mecanismos reales pertenece a una etapa posterior.

## ¿Qué significa que el monitor sea de solo lectura?

Que puede consultar el estado, pero no recibe el token ni controles para modificarlo. Las escrituras están restringidas al origen local autorizado.

## ¿Qué impide duplicar una acción si se repite una petición?

Cada acción lleva un identificador único. La tabla `requests` conserva la respuesta para que una retransmisión no vuelva a ejecutar la operación ni duplique registros.

---

# Última revisión antes de exponer

- No presentar el simulador como reconocimiento real.
- No confundir confianza de 0,85 con exactitud del 85 %.
- No afirmar que existen dataset, modelo entrenado, Arduino o cerradura física.
- No presentar los diez ciclos reales como ya ejecutados.
- No describir como observado el proceso de una institución antes de realizar el trabajo de campo.
- Si una pregunta supera la evidencia disponible, explicar el alcance confirmado y la validación necesaria.
