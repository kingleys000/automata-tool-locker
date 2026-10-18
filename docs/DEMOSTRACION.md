# Guion de operación y exposición

Requisito previo: cámara real activa y modelo propio cargado. La tablet debe mostrar `/monitor`; el operador usa `/control` en `127.0.0.1`. Cada sensor se confirma manualmente en este prototipo.

En la tablet horizontal pulsa **Ampliar diagramas** para mostrar los dos autómatas completos. **Vista completa** vuelve al resumen e historial. Las horas se muestran en America/Bogota.

## Préstamo correcto

1. Coloca el martillo en la zona de la cámara. Activa **Sensor de presencia**; deja **Sensor conectado** activo. La puerta virtual empieza cerrada.
2. Espera reconocimiento estable de martillo. Introduce `1001` y pulsa **Solicitar martillo**.
3. Señala en la tablet: inventario Disponible → Reservada; operación Inactiva → Abriendo; LED verde.
4. Pulsa **Confirmar puerta abierta**. Señala Esperando retiro.
5. Retira el martillo de la imagen y desactiva el sensor de presencia. Espera reconocimiento estable de Vacío.
6. Pulsa **Cerrar y verificar**, después **Confirmar puerta cerrada**.
7. Mantén la zona vacía dos segundos más. Señala Verificando → Completada e inventario Reservada → Prestada. Se crea un solo préstamo y el LED pasa a rojo.
8. Pulsa **Finalizar operación** para volver a Inactiva.

## Devolución correcta

1. Conserva el código del responsable `1001`. Con caja virtual vacía y cerrada, pulsa **Iniciar devolución**.
2. Confirma la puerta abierta. Coloca el martillo en la zona y activa el sensor de presencia.
3. Espera reconocimiento estable. Pulsa **Cerrar y verificar** y confirma el cierre.
4. Mantén el martillo visible durante la comprobación posterior al cierre. El inventario pasa a En revisión y se cierra el préstamo.
5. Pulsa **Finalizar operación**. Cambia el código a `ADMIN`, abre la revisión del encargado y pulsa **Aprobar** para devolver la herramienta a Disponible.

## Casos para explicar el autómata

- **Cancelar:** después de solicitar y abrir, deja el martillo dentro, conserva presencia y pulsa Cancelar reserva; confirma cierre. No se crea préstamo.
- **Herramienta incorrecta:** durante devolución coloca el alicate; el botón de cierre envía una acción que el motor rechaza y el préstamo sigue abierto. Corrige el objeto y continúa.
- **Retirar antes de terminar:** coloca el martillo, solicita y confirma cierre, pero retíralo antes de que estabilice la comprobación final. No debe pasar a En revisión.
- **Sensor contradictorio:** durante verificación desactiva presencia; se produce Incidencia aunque la cámara vea el martillo.
- **Desconexión:** detén cámara o desactiva Sensor conectado durante una operación. Reconecta, revisa valores y pulsa Reintentar. Si la puerta estaba cerrada, confirma nuevamente apertura.
- **Daño:** después de devolver y finalizar, usa ADMIN → Registrar daño. Luego Registrar reparación devuelve a En revisión, no directamente a Disponible.
- **Tablet desconectada:** desactiva su Wi-Fi unos segundos. Debe mostrar información desactualizada; al reconectar recuperará estado y eventos sin repetirlos.

## Mensaje académico

“Los estados y transiciones que se ven aquí son los mismos que ejecuta el programa. La cámara aporta observaciones; solo el autómata puede autorizar una transición. La base de datos guarda el responsable, los préstamos y el historial. En esta primera etapa los sensores y la puerta están simulados, por lo que demostramos la lógica del proceso, no la custodia física de la herramienta.”

Completa diez ciclos con el celular y exporta el historial CSV como evidencia. Los tests automatizados usan observaciones controladas y se presentan por separado.
