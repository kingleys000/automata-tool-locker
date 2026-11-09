# Contenido para la presentación de los tres avances

Guion de contenido para integrar en la plantilla PowerPoint oficial. Conservar el tema y los espacios previstos por la profesora. La distribución siguiente es orientativa y puede repartirse en las diapositivas de la plantilla. El documento desarrollado corresponde a los tres avances Markdown; esta síntesis mantiene el mismo alcance.

## 1 Proyecto y alcance

Sistema de préstamo de herramientas basado en autómatas finitos y verificación visual.

- Una unidad de martillo y un servidor local.
- Control en computador y monitor de lectura.
- Puerta y sensores simulados.

Nota oral: mencionar institución e integrantes cuando estén confirmados. El simulador didáctico funciona independientemente del módulo visual.

## 2 Objetivos

Controlar y registrar el ciclo de préstamo mediante un modelo de estados verificable.

- Modelar inventario, operación y trazas.
- Implementar motor, persistencia e interfaces.
- Preparar y evaluar un clasificador propio.
- Documentar pruebas y diez ciclos con cámara real.

## 3 Enfoque metodológico

Desarrollo aplicado e iterativo de un prototipo de software.

Comparar tres niveles: corrección del modelo, comportamiento del software y desempeño con cámara. Mostrar la relación entre objetivos, fases y evidencias del Avance 3.

## 4 Fases y productos

| Fase | Producto |
|---|---|
| Análisis | Actores y requisitos |
| Diseño | Arquitectura, modelos y pantallas |
| Construcción | Prototipo y preparación del modelo |
| Validación | Pruebas, métricas y registros |
| Documentación | Informe, anexos y sustentación |

Nota oral: usar el cronograma relativo de PLAN_TRABAJO; sustituirlo por fechas reales al conocer la entrega.

## 5 Situación y actores

Necesidad planteada: conocer disponibilidad, responsable y estado de devolución de una herramienta.

Usuario: solicita y devuelve. Encargado: revisa y aprueba o registra daño. Operador: configura la demostración. Observador: consulta el monitor.

Nota oral: las dificultades reales del laboratorio deben respaldarse con observación. Evitar afirmar pérdidas o demoras cuantificadas sin registro.

## 6 Requisitos representativos

- Solicitar, registrar retiro y verificar devolución.
- Pasar una devolución a revisión humana.
- Conservar estado y eventos.
- Rechazar transiciones inválidas.
- Impedir préstamos activos duplicados.
- Mantener monitor de solo lectura.

Nota oral: mostrar un requisito y su criterio de aceptación del Avance 4.

## 7 Caso de uso de devolución

Responsable del préstamo inicia devolución, deposita martillo y solicita cierre. El sistema exige evidencia posterior al cierre y registra el retorno. El encargado revisa y aprueba o marca daño.

Insertar el diagrama de casos de uso del Avance 4. Explicar la alternativa de objeto incorrecto y el resultado En revisión.

## 8 Arquitectura

Insertar el diagrama de arquitectura del Avance 5. Recorrer navegador, Flask, motor, cámara/adaptador y SQLite. Mostrar que el monitor consulta al mismo servidor.

Nota oral: el navegador presenta el estado; la decisión sobre transiciones corresponde al motor.

## 9 Autómatas y trazas

Inventario: Disponible, Reservada, Prestada, En revisión y Fuera de servicio.

Operación: apertura, espera de retiro o depósito, cierre, verificación y finalización; incluye incidencia y recuperación.

Ejemplo de ciclo aceptado: solicitud_verificada, retiro_verificado, devolucion_verificada, aprobacion.

Nota oral: abrir los diagramas del simulador para recorrer esa secuencia y explicar la diferencia entre el controlador y el reconocedor.

## 10 Datos

Insertar el modelo de datos del Avance 5.

Usuarios, préstamos, eventos, estado y solicitudes. Una relación lógica asocia usuario con préstamo. El índice parcial evita dos préstamos activos de la misma herramienta.

Nota oral: el esquema actual no declara una FK explícita en loans.user_code. No presentar una restricción de base de datos inexistente.

## 11 Interfaces

Mostrar capturas del control y monitor con sus títulos. El control permite operar; el monitor muestra diagramas e historial. Las capturas de pruebas existentes contienen observaciones controladas.

Nota oral: identificar controles, información disponible y actor que usa cada pantalla.

## 12 Evidencia y próximos hitos

47 pruebas automatizadas aprobadas en la ejecución del 5 de noviembre de 2026.

Pendientes: confirmar contexto institucional, capturar dataset, entrenar/evaluar el modelo y documentar diez ciclos con cámara real. La construcción del mecanismo físico corresponde a otra etapa.

Nota oral: usar los instrumentos adjuntos para explicar cómo se obtendrá la evidencia pendiente y declarar el apoyo de IA según la política docente.
