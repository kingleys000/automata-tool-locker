# Apuntes para exponer los avances 3, 4 y 5

**Proyecto:** Sistema de préstamo de herramientas basado en autómatas finitos y verificación visual.  
**Presentación:** `docs/sustentacion_avances.html`  
**Duración estimada:** 13 min 45 s, más preguntas.  
**Idea central:** no desarrollamos solamente una cámara que reconoce objetos; diseñamos un sistema que decide, registra y protege el ciclo completo de préstamo.

## Cómo usar estos apuntes

- El texto en negrita resume la idea que debe quedar clara.
- Los párrafos son una guía: habla con naturalidad, no los leas literalmente.
- En la presentación, pulsa **N** para consultar las notas y **F** para pantalla completa.
- Los tiempos son orientativos. Si necesitas reducir la exposición, acorta las escenas 3, 5, 11 y 12.

---

## Apertura — 2 min 05 s

### 1. Una herramienta. Control total. — 35 s

**Abrir presentando el propósito, no la tecnología.**

> Este proyecto busca controlar el préstamo y la devolución de una herramienta en un laboratorio académico. Para eso combinamos tres elementos: autómatas finitos que determinan qué operaciones son válidas, evidencia visual que ayuda a comprobar lo ocurrido y una base de datos que conserva el historial.
>
> El alcance es deliberadamente concreto: una unidad de martillo, funcionamiento local y hardware de puerta y presencia simulado. Durante la presentación veremos cómo se construyó, qué problema resuelve y cómo se diseñó.

**Frase puente:** “Para entender por qué necesitamos esa combinación, empecemos por tres preguntas”.

### 2. El problema en tres preguntas — 50 s

**Disponibilidad, responsabilidad y revisión.**

> La primera pregunta es si la herramienta está disponible. Una misma unidad no debería aparecer prestada a dos personas al mismo tiempo.
>
> La segunda es quién responde por ella. El sistema debe conservar el responsable, los tiempos y los eventos necesarios para reconstruir el ciclo.
>
> La tercera es si volvió en condiciones adecuadas. Por eso una devolución registrada no significa que la herramienta quede inmediatamente disponible: debe pasar por revisión humana.
>
> Estas necesidades se plantean para un laboratorio académico. El procedimiento concreto de una institución todavía debe validarse mediante trabajo de campo; no presentamos ese contexto como una observación ya realizada.

**Frase puente:** “Los tres avances convierten esas preguntas en una solución verificable”.

### 3. Tres avances, una sola historia — 40 s

**Explicar la relación entre las entregas.**

> El Avance 3 responde cómo trabajamos: define el enfoque, las fases, los instrumentos y los criterios de validación.
>
> El Avance 4 responde qué debe resolver el sistema: identifica actores, requisitos, procesos y excepciones.
>
> El Avance 5 responde cómo se materializa: presenta la arquitectura, los autómatas, el modelo de datos y las interfaces.
>
> Por tanto, no son tres documentos aislados. El análisis define reglas, el diseño las representa y la metodología establece cómo comprobarlas.

---

## Avance 3 — Metodología · 1 min 45 s

### 4. Del problema a la evidencia — 60 s

**Recorrer las cinco fases de izquierda a derecha.**

> Adoptamos un enfoque de investigación aplicada, iterativo y con evaluación experimental. Es aplicado porque busca resolver una necesidad concreta, e iterativo porque una prueba o un rechazo puede obligarnos a corregir una regla, una interfaz o un procedimiento.
>
> La primera fase es el análisis: delimitar actores, proceso, alcance y requisitos verificables.
>
> La segunda es el diseño: formalizar las reglas mediante autómatas y establecer una única autoridad de estado.
>
> La tercera es la construcción: motor, persistencia SQLite, portal, monitor y simulador independiente.
>
> La cuarta es la validación, separando tres niveles: pruebas de software, evaluación del reconocimiento visual y operación con dispositivos reales.
>
> La quinta es la documentación y presentación, conservando la relación entre objetivos, evidencias y limitaciones.

**Idea de cierre:** “El método evita que una simulación se presente como una prueba física”.

### 5. No todo lo que existe ya está validado — 45 s

**Esta distinción demuestra rigor académico.**

> Utilizamos tres estados para hablar de la evidencia. Implementado significa que existe código, documentación o una evidencia identificable en el repositorio.
>
> Documentado como ejecutado significa que una prueba quedó registrada previamente, con su alcance y procedencia; no equivale a decir que la acabamos de repetir.
>
> Pendiente significa que todavía requiere intervención del equipo, validación contextual o dispositivos reales.
>
> Esta separación es fundamental: que el código tenga una capacidad no significa que ya exista un resultado experimental. Por ejemplo, tener scripts de entrenamiento no equivale a tener un modelo entrenado ni una exactitud medida.

**Frase puente:** “Con esa disciplina de evidencia, el Avance 4 traduce el problema a requisitos concretos”.

---

## Avance 4 — Análisis del problema · 2 min 15 s

### 6. El problema se convierte en reglas observables — 60 s

**Primero actores; después requisitos.**

> Identificamos cinco actores. El usuario solicita, retira y devuelve. El encargado inspecciona y decide si aprueba, registra un daño o certifica una reparación. El operador local configura el computador, la cámara y la región de interés.
>
> Los otros dos actores son técnicos: el subsistema de visión aporta observaciones y el adaptador de puerta y sensores reporta señales físicas. Ninguno de los dos decide por sí solo qué operación es válida.
>
> Los diez requisitos funcionales se pueden resumir en cuatro compromisos: un préstamo activo por herramienta, devolución exclusivamente por el titular, rechazo de acciones inválidas sin cambiar el estado y revisión humana antes de volver a disponible.
>
> Los siete requisitos no funcionales agregan determinismo, integridad, autorización local, persistencia atómica, actualización del monitor, evidencia reciente y autonomía sin internet.

**Aclaración si preguntan:** los códigos `1001`, `1002` y `ADMIN` son demostrativos, no autenticación institucional.

### 7. Un ciclo, cinco compromisos — 75 s

**Pulsar “Reproducir ciclo” y narrar las transiciones.**

> El ciclo comienza en Disponible, con el martillo presente y evidencia visual estable. Cuando un usuario válido solicita el préstamo, el inventario pasa a Reservada y la operación coordina la apertura.
>
> Después del retiro no basta con cerrar la puerta. El sistema exige confirmación de cierre y evidencia visual nueva de que la casilla quedó vacía. Solo entonces registra el préstamo y cambia a Prestada.
>
> Para devolver, el código debe corresponder al responsable del préstamo activo. Después del depósito y del cierre, se exige evidencia posterior al cierre de que el martillo está presente.
>
> Una devolución válida cierra el préstamo, pero lleva el inventario a En revisión. El encargado puede aprobarla para regresar a Disponible, reportar daño para enviarla a Fuera de servicio o registrar una reparación, que nuevamente exige revisión.
>
> Si la evidencia es incorrecta, se pierde la conexión o se agota el tiempo, la operación entra en Incidencia y no se libera erróneamente el inventario.

**Recordar decir:** “La puerta y el sensor de presencia están simulados; esta animación explica la lógica, no una medición con cámara real”.

---

## Avance 5 — Diseño de la solución · 4 min 40 s

### 8. Dos máquinas, una única autoridad — 80 s

**Justificar por qué existen dos autómatas.**

> El diseño separa dos responsabilidades. El autómata de inventario responde en qué condición administrativa está el martillo: Disponible, Reservada, Prestada, En revisión o Fuera de servicio.
>
> El autómata de operación coordina el paso físico que sigue: Inactiva, Abriendo, Esperando retiro, Esperando depósito, Cerrando, Verificando, Completada o Incidencia.
>
> Esta separación evita mezclar, por ejemplo, que la herramienta esté prestada con el hecho de que una puerta se esté cerrando.
>
> Ambos modelos son deterministas: para cada estado y evento definido existe como máximo un siguiente estado. Una entrada no definida se rechaza sin alterar el estado actual.
>
> Además, el reconocedor de trazas incluye un estado Error absorbente. Permite comprobar si una secuencia histórica es válida y termina en Disponible. Este reconocedor académico no debe confundirse con el controlador interactivo, que simplemente rechaza una acción inválida sin incorporarla a una traza aceptada.

**Frase corta para recordar:** “Inventario dice cómo está la herramienta; operación dice qué está ocurriendo”.

### 9. La cámara observa; el motor decide — 60 s

**Explicar que una predicción aislada no autoriza una operación.**

> La cámara entrega una etiqueta, una confianza, un identificador de fotograma y una marca temporal. El motor evalúa si esa observación sirve como evidencia para la operación actual.
>
> La configuración exige una confianza mínima de 0,85, estabilidad durante al menos dos segundos, cinco cuadros consecutivos con la misma etiqueta y observaciones recientes, con una caducidad de 1,5 segundos.
>
> Después del cierre, la evidencia debe ser posterior a ese evento. Así evitamos autorizar un retiro o una devolución usando una imagen anterior. Si no hay evidencia concluyente dentro de los doce segundos configurados, se genera una incidencia.
>
> Estos números son parámetros de configuración, no métricas de exactitud. Además, el clasificador distingue categorías; no identifica una unidad específica ni determina automáticamente si está dañada.

**Aclaración necesaria:** “Como todavía no existe el modelo propio, el bloqueo de operaciones que exigen evidencia visual es el comportamiento esperado”.

### 10. Cada capa tiene una responsabilidad — 70 s

**Seguir el recorrido de las flechas.**

> El Centro de Control local puede enviar acciones, pero debe cumplir restricciones de origen, dirección loopback y un token de control. El monitor de la tablet solamente consulta el estado y no recibe ese token.
>
> Flask y Waitress exponen la API local. El motor concentra las decisiones: serializa operaciones, aplica los autómatas, gestiona solicitudes repetidas y ejecuta la verificación temporal.
>
> La cámara y el adaptador de hardware funcionan como módulos separados. El motor no supone que una orden de abrir o cerrar ya se ejecutó: espera la confirmación correspondiente del sensor.
>
> SQLite conserva estado, préstamos, eventos y solicitudes. El sistema funciona localmente, sin depender de servicios externos.
>
> El simulador didáctico usa el puerto 8001 y memoria RAM. Comparte las definiciones de los autómatas, pero no modifica la base del prototipo principal, que utiliza el puerto 8000.

**Idea de cierre:** “La arquitectura permite reemplazar posteriormente el hardware simulado sin trasladar las reglas de negocio a la cámara o a la interfaz”.

### 11. La decisión cambia; la evidencia permanece — 55 s

**Destacar integridad, auditoría e idempotencia.**

> El modelo contiene cinco tablas. `users` almacena los roles demostrativos; `loans`, los préstamos y sus tiempos; `events`, la auditoría secuencial; `state`, el estado global; y `requests`, las respuestas asociadas a identificadores únicos.
>
> La regla de integridad más importante es el índice único parcial sobre `loans`: mientras `returned_at` sea nulo, el préstamo está activo y SQLite impide otro préstamo activo para la misma herramienta.
>
> `requests` aporta idempotencia: si una petición se repite por un problema de red, se devuelve la respuesta anterior sin ejecutar dos veces la acción.
>
> `events` conserva tanto aceptaciones como rechazos, incluyendo estado anterior, estado resultante, origen y mensaje. La relación entre usuarios y préstamos se valida en Python; no afirmamos que exista una llave foránea que no está definida en SQLite.

### 12. Controlar y observar no son lo mismo — 45 s

**Relacionar interfaz, actor y permiso.**

> El Centro de Control muestra únicamente las acciones aplicables al estado actual, el selector de usuario demostrativo, la cámara, la región de interés y las señales simuladas. También concentra las acciones de revisión del encargado.
>
> El monitor presenta los autómatas sincronizados y el estado de conexión, pero no incluye botones de mutación ni token de escritura.
>
> El simulador 3D permite exponer cinco escenarios —ciclo completo, objeto incorrecto, fallo y recuperación, daño y reparación, y cancelación— sin necesitar cámara ni alterar los préstamos almacenados.

---

## Evidencia y continuidad — 1 min 55 s

### 13. Lo que podemos afirmar, y lo que todavía no — 55 s

**Leer la cifra siempre junto con su alcance.**

> La ejecución documentada del 5 de noviembre de 2026 registra 47 pruebas automatizadas aprobadas en 0,62 segundos. Estas pruebas cubren lógica, persistencia, permisos, recuperación y simulador mediante observaciones controladas.
>
> No representan exactitud del modelo de visión, funcionamiento de una cerradura física ni resultados en un laboratorio real.
>
> Sí podemos afirmar que el motor, los autómatas, el almacenamiento y las interfaces están implementados y que existe un simulador independiente.
>
> Todavía no podemos afirmar que el reconocimiento propio esté evaluado: el dataset y el archivo `models/herramientas.pt` permanecen pendientes. Tampoco existe custodia electromecánica física en esta etapa.

**Frase útil:** “Una prueba automatizada demuestra el comportamiento que evalúa, no todos los comportamientos imaginables”.

### 14. El prototipo está acotado; la ruta es concreta — 60 s

**Cerrar los pendientes con acciones verificables.**

> El primer paso es validar el contexto: identificar el laboratorio, observar el procedimiento real y confirmar actores y reglas con autorización.
>
> El segundo es capturar un dataset propio por sesiones para cinco clases: martillo, destornillador, alicate, vacío y otros. Las sesiones deben mantener separados entrenamiento, validación y prueba para evitar fugas de datos.
>
> El tercero es entrenar y evaluar con un conjunto de prueba independiente. Debemos conservar matriz de confusión, exactitud, falsos positivos y análisis de estabilidad temporal, sin inventar valores antes de ejecutar esa evaluación.
>
> El cuarto es realizar diez ciclos completos con cámara real, registrar también los intentos fallidos y probar la tablet en la red que se utilizará durante la demostración.
>
> Arduino, la puerta y los sensores físicos pertenecen a una etapa posterior y necesitarán diseño y validación adicionales.

---

## Cierre — 35 s

### 15. No se trata solo de ver; se trata de decidir — 35 s

> En conclusión, el aporte del proyecto no es solamente observar una herramienta. Es coordinar reglas formales, evidencia visual y memoria persistente para decidir qué operaciones son admisibles y poder reconstruir lo ocurrido.
>
> El Avance 3 establece cómo comprobar, el Avance 4 define qué controlar y el Avance 5 explica cómo se diseñó esa solución.
>
> El resultado actual es un prototipo académico funcional en su lógica y con límites explícitos, preparado para la siguiente fase de validación con datos y dispositivos reales.

**Terminar con:** “Quedamos atentos a sus preguntas”.

---

# Respuestas breves para preguntas probables

## ¿Por qué utilizar autómatas finitos?

Porque el préstamo tiene reglas discretas y secuencias que pueden formalizarse. El autómata hace explícito qué evento es válido en cada estado, permite rechazar operaciones fuera de orden y facilita probar ciclos completos e incompletos.

## ¿Por qué dos autómatas y no uno solo?

Porque disponibilidad administrativa y operación física son responsabilidades diferentes. Separarlas reduce combinaciones innecesarias y permite razonar con claridad sobre el estado del martillo y sobre la secuencia de apertura, cierre y verificación.

## ¿La cámara decide si se entrega la herramienta?

No. La cámara produce observaciones. El motor decide aplicando reglas de estado, titularidad, sensores, frescura y estabilidad temporal. Una predicción aislada no basta.

## ¿Qué significan exactamente las 47 pruebas?

Son pruebas automatizadas aprobadas en una ejecución documentada, con observaciones controladas. Comprueban aspectos del software; no son 47 pruebas físicas ni una medición de exactitud del reconocimiento.

## ¿Por qué no presentan una exactitud del modelo?

Porque todavía no existe un dataset propio ni un modelo entrenado que permita calcularla. Presentar una cifra sin esa evaluación sería inventar evidencia. Los scripts de captura, entrenamiento y evaluación ya están preparados.

## ¿La devolución deja inmediatamente disponible el martillo?

No. La devolución cierra el préstamo y cambia el inventario a En revisión. Solo el encargado puede aprobar el reingreso a Disponible después de inspeccionar físicamente la herramienta.

## ¿Qué ocurre si se deposita un objeto incorrecto?

La operación pasa a Incidencia, el préstamo permanece activo y el inventario no se libera. El procedimiento contempla corrección y reintento; el intento queda registrado.

## ¿El sistema ya controla una puerta real?

No. La puerta y la presencia están simuladas mediante `SimulatedHardware`. El diseño separa el adaptador para facilitar una integración posterior, pero esta requerirá construcción y validación física.

## ¿El monitor de la tablet puede controlar el sistema?

No. Solo consulta información. Las mutaciones exigen origen local, dirección loopback y token; el monitor no recibe ese token ni controles de escritura.

## ¿Qué limita la generalización de los resultados?

El alcance de una unidad, la ausencia de validación contextual, el uso de hardware simulado y la falta de evaluación con cámara real. Además, un modelo evaluado en una escena no se generaliza automáticamente a otra cámara, iluminación o institución.

---

# Recordatorio final para la sustentación

- No llamar “reconocimiento real” a una demostración del simulador.
- No presentar 0,85 de confianza como si fuera 85 % de exactitud.
- No confundir los diez ciclos automatizados con los diez ciclos reales pendientes.
- No afirmar que existe Arduino, cerradura física, dataset o modelo entrenado.
- No describir el proceso de una institución como observado hasta aplicar el instrumento de campo.
- Si una pregunta excede la evidencia disponible, responder con el alcance confirmado y explicar qué validación haría falta.
