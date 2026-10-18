# Estado para continuar el proyecto

Revisado el 18 de octubre de 2026.

## Alcance encontrado

Prototipo académico de préstamo de una unidad de martillo: control local en el computador, monitor de lectura en tablet, dos autómatas, cámara real y puerta/sensores simulados. El alcance guardado en README e INFORME sitúa la electrónica física en una etapa posterior.

## Implementado y comprobado

- Autómatas, préstamos, devolución, revisión del encargado, incidencias y recuperación con SQLite.
- Portal, diagramas, historial CSV, control local y sincronización del monitor.
- Captura de imágenes, separación de sesiones, entrenamiento y evaluación mediante scripts.
- 36 pruebas automatizadas aprobadas; incluyen diez ciclos del motor con observaciones controladas.
- Ciclo completo en Edge con dos páginas sincronizadas: actualización observada de 96 ms.
- Vistas de escritorio, tablet horizontal/vertical y móvil, y pérdida/recuperación de conexión verificadas.
- Dependencias sin conflictos según `pip check`.

## Correcciones de esta revisión

- El formulario de cámara antes mostraba siempre índice 0 y ROI completa. Ahora carga la configuración efectiva y conserva los valores de la sesión al recargar. Se añadió una prueba de regresión.
- Pytest busca pruebas únicamente en `tests/`, sin recorrer artefactos temporales de otras sesiones.
- La comprobación visual acepta una URL como tercer argumento para ejecutarse contra un servidor aislado.

## Pendiente que requiere herramientas y dispositivos reales

1. Conectar el celular mediante DroidCam, fijar la escena y seleccionar cámara/ROI.
2. Capturar las cinco clases: martillo, destornillador, alicate, vacío y otros. Al revisar no existía la carpeta `dataset/`: hay cero imágenes disponibles.
3. Validar el dataset y entrenar. No existe `models/herramientas.pt`; por eso el portal no puede autorizar préstamos reales todavía.
4. Evaluar el modelo, documentar las métricas y completar diez ciclos con cámara real.
5. Verificar el monitor desde la tablet y la red que se usarán en la exposición.

Las instrucciones están en [RECONOCIMIENTO.md](RECONOCIMIENTO.md) y [DEMOSTRACION.md](DEMOSTRACION.md). Los resultados de tests no sustituyen estas mediciones. No se conectó ni activó una cámara durante esta revisión.

## Inicio

Desde la carpeta del proyecto:

```powershell
.\.venv\Scripts\python.exe run.py
```

Abrir `http://127.0.0.1:8000/control`. El servidor de pruebas utilizado en la revisión ya se detuvo.

## Registro y continuidad

La carpeta contiene un repositorio Git sin commits; los archivos de código todavía aparecen como no rastreados. No hay un historial Git para reconstruir requisitos de la conversación anterior. Esta revisión se basó en los archivos guardados. Se conservaron la base de préstamos y los datos existentes.
