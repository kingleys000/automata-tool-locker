# Módulo de simulación visual

Implementado y verificado el 19 de octubre de 2026.

## Iniciar

Desde la carpeta del proyecto, ejecuta:

```powershell
.\.venv\Scripts\python.exe run_simulador.py
```

También puedes usar `iniciar_simulador.ps1`. Usa las dependencias básicas de `requirements.txt`: Flask y Waitress. No necesita OpenCV, PyTorch, cámara, imágenes ni un modelo entrenado. Los recursos visuales se sirven desde el computador y no requieren internet.

| Dispositivo | Dirección | Contenido |
|---|---|---|
| Computador | `http://127.0.0.1:8001/simulador` | Compartimiento 3D, controles, autómatas e historial |
| Tablet | `http://IP_DEL_COMPUTADOR:8001/automatas` | Dos autómatas sincronizados, última transición y explicación del evento |

Las direcciones candidatas de la tablet aparecen al final de la vista del computador. Ambos equipos deben estar en la misma red. Si Windows solicita acceso de red, permite el acceso en la red privada utilizada para la demostración. El botón **Pantalla completa** aprovecha la pantalla de la tablet. En horizontal, los diagramas se muestran lado a lado; en vertical se apilan.

El puerto puede cambiarse con `--port 8002`. Para limitarlo al computador, añade `--host 127.0.0.1`.

## Explorar manualmente

El estado inicial contiene un martillo, puerta cerrada, sensor conectado e inventario Disponible. **Avanzar un paso** ejecuta la siguiente acción del ciclo:

1. Solicitar martillo → inventario Reservada y operación Abriendo.
2. Abrir puerta → Esperando retiro.
3. Retirar martillo → la herramienta sale de la escena interior.
4. Ordenar cierre → Cerrando.
5. Confirmar puerta cerrada → Verificando.
6. Verificar contenido vacío → Prestada y Completada.
7. Finalizar → Inactiva, con el préstamo activo.
8. Iniciar devolución → Abriendo.
9. Abrir puerta → Esperando depósito.
10. Depositar martillo.
11. Ordenar cierre.
12. Confirmar cierre.
13. Verificar contenido → En revisión y Completada.
14. Finalizar operación.
15. Aprobar herramienta → Disponible.

**Acciones y situaciones manuales** permite elegir otras acciones: cancelar una reserva, depositar un alicate o destornillador, desconectar el sensor, registrar daño o reparación. Una acción incompatible se rechaza y explica por qué. La comprobación evalúa el objeto virtual y los sensores del simulador.

Las flechas de **Perspectiva** giran la escena. La puerta, la herramienta y el cambio de perspectiva utilizan transformaciones 3D con animaciones. Los diagramas resaltan el estado activo y animan el recorrido de la última transición. Se respeta la preferencia de movimiento reducido del navegador.

## Demostraciones automáticas

**Reproducir desde inicio** reinicia la simulación y ejecuta el escenario seleccionado:

- **Ciclo completo:** préstamo y devolución correctos.
- **Objeto incorrecto:** intento de cierre con alicate, rechazo y corrección con martillo.
- **Fallo y recuperación:** sensor desconectado durante la verificación, Incidencia y reintento.
- **Daño y reparación:** En revisión → Fuera de servicio → En revisión → Disponible.
- **Cancelar reserva:** se conserva el martillo dentro y se libera la reserva sin crear préstamo.

**Pausar** detiene el avance automático. Durante la pausa, **Avanzar un paso** ejecuta un paso del escenario y **Continuar** reanuda la reproducción. El ritmo puede cambiarse entre 3, 1,8 y 0,8 segundos por acción. **Reiniciar simulación** vuelve al modo libre.

La reproducción ocurre en el servidor: continúa aunque el navegador del computador pierda el foco o se cierre. La tablet representa el mismo estado. Si se pierde la conexión, muestra un aviso; al reconectar recupera el estado actual.

## Independencia del módulo original

- `run.py`, el puerto 8000, el portal de cámara y su base `data/prestamos.sqlite` conservan su funcionamiento.
- `run_simulador.py` utiliza otro servidor y guarda su estado únicamente en memoria. Se pierde al cerrar o reiniciar ese servidor.
- Ambos módulos comparten las definiciones de estados y transiciones de `app/automata.py`.
- El simulador no crea observaciones para el motor de cámara ni accede a su base de préstamos.
- El control solo se entrega mediante localhost/loopback, y las escrituras requieren el token de la vista del computador. La tablet recibe una vista de lectura.

## Verificación

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_simulator.py -q -p no:cacheprovider
node tests/simulator_browser.cjs
```

Para el navegador se requiere Playwright y Edge. Si Playwright está en otra carpeta, pasa la ruta de su módulo como segundo argumento. La prueba inicia su propio simulador temporal en `127.0.0.1:8102` y lo cierra al terminar.

Resultados ejecutados: **47 pruebas aprobadas en la suite conjunta**, incluidas 11 del simulador. Estas últimas cubren los cinco escenarios, diez ciclos manuales, pausa/paso/reanudación, idempotencia, entradas inválidas y permisos de la tablet. La prueba de Edge comprobó un ciclo manual completo, demostración automática con fallo y recuperación, dos páginas sincronizadas, reconexión y diseños de escritorio (1440×1000), tablet (1280×800 y 800×1280) y móvil (390×844). Las capturas están en `artifacts/simulador-*.png`.

La sincronización se comprobó con dos páginas en el mismo computador. La conexión con una tablet física depende de la red local y debe verificarse en el lugar de la demostración.
