# Preparar el reconocimiento con tus herramientas

## 1. Conectar el celular

Instala DroidCam desde su fuente oficial en Android y el cliente de Windows: <https://droidcam.app/windows/>. Sigue la conexión USB de <https://droidcam.app/help/>. El cable debe permitir datos; según el celular, necesitarás depuración USB y su controlador. Autoriza únicamente el computador que usarás.

Fija el celular de frente a una zona de fondo uniforme. Evita reflejos y sombras fuertes. Abre DroidCam; en `/control` selecciona el índice de cámara y pulsa **Iniciar cámara**. Si se muestra otra cámara, deténla y cambia el índice. No se necesita una caja física todavía.

El rectángulo verde indica la región de interés. Se recorta esa región y se rellena hasta formar un cuadrado sin cortar la herramienta; ese mismo preprocesamiento se utiliza en las capturas y la inferencia. No muevas el celular después de capturar el dataset sin volver a validar.

## 2. Dataset propio

En **Preparar las imágenes de entrenamiento**, selecciona clase, conjunto y sesión; pulsa **Guardar imagen real**. No hay captura automática de rostros ni subida de imágenes a un servicio externo.

Clases exactas: `martillo`, `destornillador`, `alicate`, `vacio`, `otros`.

Objetivo inicial: unas **100 imágenes por clase**, distribuidas aproximadamente en 60 para entrenamiento, 20 para validación y 20 para prueba. Para entrenar una prueba preliminar, el script exige como mínimo 10/5/5 imágenes por clase. Eso comprueba estructura, no garantiza precisión.

Sesiones sugeridas:

| Sesión | Conjunto | Capturas |
|---|---|---|
| `entreno_01`, `entreno_02`, `entreno_03` | train | Distintas colocaciones y condiciones previstas |
| `validacion_01` | val | Otra sesión, sin copiar imágenes de entrenamiento |
| `prueba_01` | test | Sesión reservada para evaluación final |

Una sesión no puede pertenecer a dos conjuntos. No distribuyas fotogramas casi idénticos de una misma toma entre train/val/test. El portal y el script comprueban los nombres de sesión, pero la independencia física de las capturas depende de cómo las tomes.

Incluye pequeñas variaciones de orientación, posición, escala e iluminación. `otros` debe contener manos, objetos ajenos y objetos tapados que deseas rechazar. `vacio` debe mostrar la zona realmente vacía en condiciones diferentes. No introduzcas etiquetas, colores de fondo exclusivos o textos que permitan adivinar la clase sin mirar la herramienta.

```text
dataset/
  sessions.json
  train/martillo/entreno_01__fecha.jpg
  train/destornillador/...
  train/alicate/...
  train/vacio/...
  train/otros/...
  val/<las cinco clases>/...
  test/<las cinco clases>/...
```

## 3. Validar y entrenar

Detén la cámara para liberar recursos y ejecuta:

```powershell
.\.venv\Scripts\python.exe tools/train_model.py --check
.\.venv\Scripts\python.exe tools/train_model.py --epochs 40 --device cpu
```

El primer entrenamiento puede descargar `yolo11n-cls.pt`. Ese modelo base se ajusta con tus cinco clases; no se usa directamente como si reconociera las miniaturas. El entrenamiento usa validación para elegir `best.pt`, que se copia a `models/herramientas.pt`. Se guarda también `models/entrenamiento.json`.

Si el computador tarda demasiado, puedes ejecutar el mismo script y dataset en una sesión Colab con GPU, usando `--device 0`, y copiar el modelo resultante al computador. Esa alternativa requiere transferir voluntariamente tus imágenes a Colab. No está activada ni es necesaria para operar el portal local.

## 4. Evaluar antes de demostrar

```powershell
.\.venv\Scripts\python.exe tools/evaluate_model.py
```

Se generan `artifacts/evaluacion_modelo.json` y `artifacts/predicciones.csv`, con matriz de confusión, exactitud y falsos positivos de martillo. No contienen valores ficticios: solo se crean después de evaluar un modelo existente.

Usa **val** para corregir datos, entrenar y ajustar el umbral. Reserva **test** para la evaluación final; si ajustas repetidamente según sus resultados, necesitarás un nuevo test independiente.

El portal exige puntuación ≥ 0,85, al menos cinco observaciones consecutivas y un intervalo de al menos dos segundos. Descarta observaciones antiguas, repetidas por identificador o fuera de orden. Después del cierre exige un intervalo nuevo. La puntuación no es una probabilidad calibrada de acierto.

Detén e inicia la cámara para cargar el modelo. Prueba las cinco clases, objetos parcialmente tapados y retirada antes del cierre. La aceptación del conjunto de imágenes no sustituye las pruebas del procedimiento completo.

## 5. Si falla

- **No abre cámara:** inicia DroidCam, revisa índice, cable y permisos de cámara de Windows; cierra aplicaciones que la estén usando.
- **Video pero sin modelo:** captura el dataset y entrena; revisa el nombre y las cinco clases del modelo.
- **Nunca estabiliza:** mide iluminación y rendimiento, revisa ROI y datos; no reduzcas el umbral para ocultar falsos positivos.
- **Confunde alicate y martillo:** añade ejemplos independientes de esas posiciones y vuelve a evaluar.
- **Video se corta:** la operación permanecerá pendiente; reconecta y usa Reintentar.
- **La caja física cambia la imagen:** captura nuevas sesiones a través de la ventana definitiva antes de dar por válido el modelo.
