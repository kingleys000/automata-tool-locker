# Guía docente del avance 5

Fuente: https://avance5proyectoaula.netlify.app/

Consulta: 2026-11-05. Extracción textual íntegra; se omiten estilos y scripts.

Avance 5 · Fase de Diseño

Guía Redacción y presentación de un Proyecto de aula

Avance 5: Fase de Diseño

Proyecto de Aula

Reconoce las orientaciones para definir cómo se construirá la solución: arquitectura, diseño funcional, diseño de datos e interfaces.

Entrega en dos formatos:

la Fase de Diseño debe consignarse tanto en la

plantilla Word

como en la

plantilla PowerPoint

. El Word desarrolla y explica las decisiones de diseño; el PowerPoint las sintetiza mediante esquemas, modelos y prototipos. Conserven el formato original de ambas plantillas.

Explora el avance

Inicio y entregables

A. Arquitectura

B. Diseño funcional

C. Diseño de datos

D. Interfaces

Word y PowerPoint

Uso ético de la IA

Cronograma y equipo

Lista de verificación

¿Qué deben entregar?

El Avance 5 corresponde a la sección

VIII. DISEÑO DE LA SOLUCIÓN

de la plantilla del proyecto. Esta fase debe responder la pregunta:

¿Cómo se construirá la solución?

En esta etapa todavía se explica y representa el diseño de la solución. No se debe presentar como si todo el sistema ya estuviera implementado.

Plantilla Word

Desarrollo y justificación

Expliquen los componentes del diseño, sus decisiones y la relación con los requerimientos definidos en el Avance 4.

Plantilla PowerPoint

Síntesis visual

Presenten la arquitectura, modelos, diagramas y prototipos de forma clara y legible.

Componentes indicados en la plantilla

A. Arquitectura:

estructura general del sistema y sus componentes.

B. Diseño funcional:

organización de funciones y comportamiento de la solución.

C. Diseño de datos:

modelo entidad-relación, modelo relacional, tablas y relaciones, llaves primarias y foráneas.

D. Interfaces:

prototipos de las pantallas de la solución.

Lean la descripción de cada ítem en la plantilla Word.

Esta guía explica y ejemplifica los componentes, pero no sustituye las instrucciones ni los espacios previstos en el documento oficial.

La plantilla también menciona diagramas de procesos (por ejemplo, flujo, UML o BPMN) como posibles apoyos de diseño. Seleccionen los que sean pertinentes para su proyecto y atiendan lo que solicite el ítem correspondiente.

A. Arquitectura del sistema

La arquitectura presenta la estructura general de la solución y muestra cómo se organizan sus componentes y cómo se relacionan entre sí. Debe permitir comprender la visión global del sistema.

¿Qué deben mostrar?

Los componentes principales de la solución.

La función que cumple cada componente.

La forma en que se comunican o intercambian información.

La ubicación de elementos como interfaz, lógica de negocio y base de datos, si hacen parte de la solución.

Ejemplo conceptual de arquitectura por capas

Usuario

↓

Interfaz

↓

Lógica de negocio

↓

Base de datos

Es un ejemplo simplificado tomado como referencia de la plantilla. La arquitectura real debe corresponder con las tecnologías y necesidades de cada equipo.

En el documento Word

Incluyan el diagrama de arquitectura y expliquen los componentes, sus responsabilidades y las relaciones entre ellos. No inserten una imagen sin describir qué representa.

En PowerPoint

Presenten el diagrama general en una diapositiva legible y destaquen brevemente la función de cada bloque.

Coherencia:

la arquitectura debe ser viable para el alcance del proyecto y consistente con los requerimientos, las herramientas y las tecnologías que el equipo propone utilizar.

B. Diseño funcional

Este componente explica cómo se organiza funcionalmente la solución y cómo se relacionan sus funciones para responder a las necesidades identificadas en el análisis.

¿Qué deben definir?

Los módulos, funciones o componentes funcionales principales.

Qué responsabilidad tendrá cada uno.

Cómo se relacionan con los requerimientos funcionales definidos en el Avance 4.

El flujo general de las operaciones relevantes, cuando ayude a comprender el funcionamiento.

Ejemplo orientador para un sistema de inventario:

módulo de usuarios, módulo de productos, módulo de movimientos de inventario y módulo de reportes. Para cada uno, expliquen qué operaciones agrupa y qué necesidad atiende.

Diagramas de procesos

La plantilla señala que el diseño de procesos puede representarse mediante diagramas de flujo, UML, BPMN, entre otros. Elijan la representación que mejor explique el proceso de su solución.

En Word y PowerPoint

En Word expliquen las funciones y adjunten los diagramas pertinentes con título y descripción. En PowerPoint resuman los módulos o el flujo principal, evitando diagramas saturados.

No confundan diseño con implementación:

describir el módulo que se diseñará no significa afirmar que ya está programado o funcionando.

C. Diseño de datos

Representen cómo se organizará la información que necesita la solución. La plantilla menciona expresamente el modelo entidad-relación, el modelo relacional, las tablas, las relaciones, las llaves primarias y las llaves foráneas.

Elementos que pueden incluir

Modelo entidad-relación:

entidades, atributos y relaciones del dominio.

Modelo relacional:

representación de las tablas y sus vínculos.

Tablas:

nombre y propósito de cada tabla.

Relaciones:

cómo se conectan las tablas.

Llaves primarias (PK):

identifican de manera única los registros.

Llaves foráneas (FK):

establecen referencias entre tablas.

Ejemplo conceptual

USUARIO

(id_usuario PK, nombre, correo)

PEDIDO

(id_pedido PK, fecha, id_usuario FK)

Relación: un usuario puede registrar varios pedidos; cada pedido se asocia con un usuario.

Ejemplo ilustrativo. Las entidades, atributos y cardinalidades deben derivarse de los datos que realmente requiere el proyecto.

Preguntas para revisar el modelo

¿Las entidades representan elementos relevantes del problema?

¿Los atributos son necesarios y tienen nombres comprensibles?

¿Se identificaron las llaves primarias?

¿Las llaves foráneas corresponden con las relaciones?

¿El modelo permite almacenar la información requerida por las funciones del sistema?

En Word y PowerPoint

En Word incluyan el modelo y expliquen sus elementos y relaciones. En PowerPoint presenten el diagrama de datos con tamaño suficiente para leer nombres, llaves y cardinalidades.

D. Diseño de interfaces

Incluyan prototipos de las pantallas que tendrá la solución. La plantilla da como ejemplo una figura titulada “Diseño de la pantalla de inicio”. Los prototipos permiten visualizar cómo interactuarán los usuarios con el sistema.

¿Qué debe mostrar un prototipo?

La distribución general de la pantalla.

Los campos, botones, menús y opciones principales.

La información que el usuario podrá consultar o registrar.

La navegación o relación con otras pantallas, cuando corresponda.

Ejemplos de pantallas que podrían diseñarse

Inicio de sesión

Campos de usuario y contraseña, botón de acceso y mensajes de validación.

Panel principal

Menú de navegación y acceso a funciones principales.

Formulario de registro

Campos para ingresar datos y acciones guardar/cancelar.

Consulta o reporte

Filtros, resultados y opciones de consulta.

Cómo presentar las figuras

Inserten los prototipos con numeración y título, por ejemplo:

Fig. 1. Diseño de la pantalla de inicio.

Expliquen brevemente qué función cumple cada pantalla y qué actor la utilizará.

Importante:

un prototipo es una representación del diseño de la interfaz; no demuestra por sí solo que la pantalla ya esté implementada o conectada a una base de datos.

En PowerPoint

Seleccionen los prototipos más representativos. Asegúrense de que las imágenes se vean completas, nítidas y con textos legibles.

Entrega en Word y PowerPoint

Documento Word

Explicar y documentar

Desarrollar los apartados A, B, C y D de la sección VIII.

Describir las decisiones de diseño.

Insertar diagramas y prototipos con título y explicación.

Conservar estilos, numeración, tipografía y distribución.

Presentación PowerPoint

Comunicar visualmente

Mostrar arquitectura, diseño funcional, datos e interfaces.

Utilizar diagramas y prototipos legibles.

Incluir explicaciones breves, no bloques extensos de texto.

Conservar tema, colores, tipografías y distribución de la plantilla.

Formato de la plantilla Word

La plantilla académica indica como configuración recomendada: papel carta; Times New Roman de 10 puntos; interlineado sencillo; texto justificado; márgenes definidos en el documento; y dos columnas para el cuerpo técnico. Los títulos principales utilizan numeración romana, mayúsculas y alineación centrada; las subsecciones emplean letras (A., B., C.) y alineación a la izquierda.

No creen un documento nuevo ni modifiquen el diseño de las plantillas. Trabajen sobre los archivos oficiales y mantengan el formato establecido.

Coherencia entre archivos:

el Word y el PowerPoint deben representar el mismo diseño. Los nombres de módulos, relaciones, tablas, actores y pantallas no deben contradecirse.

Antes de cargar en Drive

Abran las plantillas oficiales indicadas por la docente.

Lean la descripción de cada ítem de la sección VIII en Word.

Verifiquen que estén incluidos los cuatro componentes del diseño.

Comprueben que los diagramas y prototipos se entiendan y tengan títulos.

Revisen que ambos archivos mantengan el formato original y sean coherentes.

Verifiquen nombres de archivo y carpeta de entrega.

Uso ético de la inteligencia artificial

La IA puede apoyar la exploración de alternativas de arquitectura, la comprensión de modelos, la revisión de diagramas o la generación de ideas para prototipos. No reemplaza las decisiones técnicas ni la responsabilidad del equipo.

Reglas indispensables

Usen la IA como apoyo, no como autora del diseño ni como fuente única.

Lean y comprendan cada propuesta antes de incorporarla.

Verifiquen que las tecnologías, diagramas, relaciones y conceptos sean correctos y adecuados al proyecto.

Comprueben que el diseño propuesto responda a los requerimientos reales del Avance 4.

No incluyan diagramas o modelos que el equipo no pueda explicar.

Declaren o citen el uso de IA según las indicaciones docentes y normas académicas aplicables.

No ingresen datos personales, sensibles o confidenciales en herramientas de IA.

Antes de cargar en Drive:

lean, verifiquen y validen toda la información proporcionada por IA. Revisen especialmente la exactitud de los diagramas, las relaciones de datos y la viabilidad de la arquitectura. El equipo responde por lo que entrega.

Preguntas para el equipo

¿Podemos explicar por qué elegimos esta arquitectura?

¿El modelo de datos representa las necesidades reales?

¿Las interfaces corresponden a las funciones propuestas?

¿Verificamos la información y adaptamos las sugerencias de IA?

Cronograma y participación de todo el equipo

Puntualidad

Consulten las fechas oficiales del cronograma y organicen entregas internas con anticipación. Reserven tiempo para integrar diagramas, revisar el documento, preparar la presentación y corregir.

Definan tareas y responsables desde el inicio.

Establezcan fechas internas anteriores al vencimiento oficial.

Revisen periódicamente el avance y las dependencias entre componentes.

No esperen al último día para insertar imágenes o consolidar versiones.

Suban los archivos dentro del plazo y comprueben que se abren correctamente.

Participación de todos y cada uno

La distribución de tareas no exime a ningún integrante de conocer el diseño completo. Todos deben aportar, revisar y poder explicar las decisiones del equipo.

Acuerdo mínimo del equipo

Todos participan en la revisión de la arquitectura.

Todos comprenden el diseño funcional y sus vínculos con los requerimientos.

Todos revisan el modelo de datos y los prototipos.

Todos conocen el contenido de Word y PowerPoint.

Todos pueden sustentar las decisiones de diseño.

Actividad

Responsables

Fecha interna

Estado

Diseñar arquitectura

Definir en equipo

Antes de entrega

Pendiente / En proceso / Listo

Definir diseño funcional

Definir en equipo

Antes de entrega

Pendiente / En proceso / Listo

Elaborar modelo de datos

Definir en equipo

Antes de entrega

Pendiente / En proceso / Listo

Diseñar prototipos

Definir en equipo

Antes de entrega

Pendiente / En proceso / Listo

Revisar Word y PowerPoint

Todo el equipo

Antes de entrega

Pendiente / En proceso / Listo

Lista de verificación antes de entregar

Marquen los criterios que el equipo ya comprobó. El indicador muestra el progreso.

0 de 16

Se desarrolló la sección VIII. Diseño de la solución.

Se elaboró y explicó el diagrama de arquitectura.

Se describieron los componentes y sus responsabilidades.

Se desarrolló el diseño funcional y sus módulos o procesos.

El diseño funcional es coherente con los requerimientos del Avance 4.

Se elaboró el modelo entidad-relación, cuando aplica.

Se identificaron tablas, relaciones, llaves primarias y foráneas.

Se diseñaron prototipos de las interfaces principales.

Los diagramas y prototipos tienen títulos y explicaciones.

Se leyó la descripción de cada ítem de la plantilla Word.

Se completó también la plantilla PowerPoint.

Word y PowerPoint muestran el mismo diseño y no se contradicen.

Se mantuvo el formato original de ambas plantillas.

Se leyó, verificó y validó la información sugerida por IA.

Se cumplió el cronograma y se comprobó la carga en Drive.

Todos los integrantes participaron y pueden explicar el diseño.

Restablecer lista

Imprimir / Guardar como PDF

Entrega responsable:

verifiquen que Word y PowerPoint sean las versiones definitivas, se abran correctamente y estén en la carpeta indicada.

Recurso de apoyo académico · Proyecto de Aula · Avance 5: Fase de Diseño
