# Laboratorio de herramientas con autómatas

Prototipo académico local: **un martillo, dos autómatas, puerta y sensores simulados, cámara real**. El computador controla las operaciones y la tablet observa los diagramas. El reconocimiento necesita imágenes de tus herramientas y un modelo entrenado; no se incluye un modelo ficticio ni se autorizan préstamos sin evidencia visual.

Revisión del 18 de octubre de 2026: [estado actual, correcciones y pendientes para continuar](docs/ESTADO.md).

## Nuevo módulo: simulador completo

El módulo independiente permite explorar los dos autómatas sin cámara ni modelo. Incluye un compartimiento 3D animado, avance manual, cinco demostraciones automáticas, pausa y cambio de velocidad.

```powershell
.\.venv\Scripts\python.exe run_simulador.py
```

- Computador: **http://127.0.0.1:8001/simulador** (escena, controles y diagramas).
- Tablet: **http://IP_DEL_COMPUTADOR:8001/automatas** (solo autómatas y sus eventos).
- También puedes ejecutar `iniciar_simulador.ps1`.

El simulador conserva su estado en memoria durante la sesión. El módulo de cámara continúa en el puerto 8000, con su base de datos propia. [Guía del simulador y comprobaciones](docs/SIMULADOR.md).

## Inicio en este computador

El entorno `.venv` contiene las dependencias instaladas durante la implementación. En PowerShell, desde esta carpeta:

```powershell
.\.venv\Scripts\python.exe run.py
```

También puedes ejecutar `iniciar.ps1`. Mantén la terminal abierta; `Ctrl+C` detiene el servidor.

- Control del computador: **http://127.0.0.1:8000/control**
- Tablet: **http://IP_DEL_COMPUTADOR:8000/monitor**, usando la misma red.
- Las direcciones candidatas para la tablet aparecen al final del control. Elige la IPv4 de la conexión Wi-Fi o Ethernet que comparten, no una VPN.
- Si Windows solicita acceso de red, habilítalo únicamente para tu red privada. No hace falta publicar en internet ni abrir puertos en el router.
- Si la tablet no conecta, comprueba que la red no aísla dispositivos invitados y consulta `ipconfig`.

## Instalación en otro equipo

Recomendado: Python **3.12 de 64 bits**, Windows 10/11 y navegador actualizado. No copies `.venv` a otro computador: recréalo.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pip install -r requirements-vision.txt
.\.venv\Scripts\python.exe run.py
```

`instalar.ps1` e `instalar_vision.ps1` automatizan esos pasos. No es necesario activar el entorno ni cambiar la política global de ejecución de PowerShell: siempre puedes ejecutar los comandos anteriores directamente. Las descargas iniciales de PyTorch y del peso base requieren internet; el portal y el modelo ya entrenado funcionan localmente.

## Primer uso

1. Abre `/control` en el computador y `/monitor` en la tablet.
2. Configura DroidCam en Android y Windows, preferiblemente por USB. Inicia DroidCam antes de iniciar la cámara en el portal.
3. Selecciona su índice de cámara y delimita una zona con fondo sencillo. La cámara solo se activa al pulsar **Iniciar cámara**.
4. Sin modelo, podrás ver video y guardar imágenes; el portal indicará **Modelo pendiente** y bloqueará los préstamos.
5. Sigue [la guía de reconocimiento](docs/RECONOCIMIENTO.md) para crear el dataset, entrenar y evaluar.
6. Detén e inicia la cámara después de guardar `models/herramientas.pt`.
7. Sigue [el guion de demostración](docs/DEMOSTRACION.md).

Usuarios de demostración: `1001`, `1002`; encargado: `ADMIN`. Son códigos académicos, no autenticación para un sistema productivo. El control de escritura se limita al computador mediante loopback, origen y token de control. La tablet no recibe el token ni puede escribir aunque intente llamar directamente a la API.

## Pruebas

`requirements-lock.txt` registra las versiones exactas instaladas y comprobadas en Python 3.12. Para reproducir este entorno puedes instalar ese archivo en lugar de los requisitos por rango.

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp=.pytest_tmp
node --check static/app.js
```

Las pruebas de lógica usan un adaptador de cámara controlado **solo dentro de los tests**. No existe un endpoint para introducir resultados de reconocimiento falsos. Diez ciclos en tests no equivalen a diez ciclos con el celular y tus herramientas.

La comprobación visual usa Playwright y Edge con el servidor iniciado: `node tests/browser_check.cjs`. Si Playwright no está en el proyecto, pasa como segundo argumento la ruta de su módulo instalado. Opcionalmente, pasa la URL del servidor como tercer argumento. Las capturas se guardan en `artifacts/`.

`node tests/browser_cycle.cjs` verifica un ciclo de interfaz en un servidor temporal independiente, con observaciones controladas solo para tests. [Resultados y límites de validación](docs/VALIDACION.md).

## Organización

- `app/automata.py`: estados y transiciones compartidos por motor y diagramas; AFD reconocedor académico.
- `app/engine.py`: validación, estabilidad visual, operaciones atómicas, préstamos y recuperación.
- `app/hardware.py`: contrato del futuro adaptador Arduino y simulador actual.
- `app/camera.py`: video real, inferencia y captura del dataset.
- `app/web.py`: API, control local y monitor de lectura.
- `templates/`, `static/`: portal adaptable y diagramas SVG sin dependencias externas.
- `tools/`: entrenamiento y evaluación.
- `docs/`: informe técnico, reconocimiento, guion y validación.
- `data/prestamos.sqlite`: estado e historial persistentes. Respáldalo con el servidor detenido.

## Configuración y límites

`config.json` define puerto, cámara, ROI, umbral, estabilidad y tiempo de verificación. Reinicia el servidor tras editarlo. Los cambios de cámara/ROI hechos en el portal duran esa ejecución; copia los valores a la configuración para conservarlos. Una nueva ROI puede requerir nuevas fotografías.

Un reinicio durante una operación produce una incidencia y borra la evidencia visual temporal. El responsable o ADMIN debe reconectar cámara/sensores, revisar el contenido y pulsar **Reintentar**. No se borran los préstamos.

El modelo comprueba apariencia, no identidad de una unidad ni daños. El sensor simulado y la ilustración de la caja no son reconocimiento. Se exige evidencia nueva después del cierre simulado, pero esta versión no prueba custodia física ni resistencia al engaño. La fuente virtual de video también debe transmitir en vivo: una imagen congelada repetida por un controlador externo puede no distinguirse de una escena estática. Al añadir la caja física se deberán validar nuevamente cámara, iluminación y sensores.

No hay Arduino ni puerta física implementados en esta etapa. El siguiente hito es validar el reconocimiento con las herramientas reales y ejecutar los diez ciclos del guion antes de construir el mecanismo.
