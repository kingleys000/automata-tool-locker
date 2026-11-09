"""Genera docs/PRESENTACION.pptx con los 13 apartados de la plantilla de anteproyecto.

Uso: .venv/bin/python tools/build_presentacion.py
"""
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt

SALIDA = Path(__file__).resolve().parent.parent / "docs" / "PRESENTACION.pptx"


def diapositiva_texto(prs, titulo, bloques, tamano=16):
    """bloques: lista de (nivel, texto)."""
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = titulo
    cuerpo = slide.placeholders[1].text_frame
    cuerpo.word_wrap = True
    for i, (nivel, texto) in enumerate(bloques):
        parrafo = cuerpo.paragraphs[0] if i == 0 else cuerpo.add_paragraph()
        parrafo.level = nivel
        parrafo.text = texto
        for run in parrafo.runs:
            run.font.size = Pt(tamano - 2 * nivel)
    return slide


def diapositiva_portada(prs, titulo, lineas):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = titulo
    slide.placeholders[1].text = "\n".join(lineas)
    return slide


def diapositiva_tabla(prs, titulo, encabezado, filas, tamano=14):
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = titulo
    filas_n = len(filas) + 1
    cols_n = len(encabezado)
    ancho = Inches(9)
    alto = Inches(0.5) * filas_n
    izquierda = Inches(0.5)
    arriba = Inches(1.5)
    tabla = slide.shapes.add_table(filas_n, cols_n, izquierda, arriba, ancho, alto).table
    for j, texto in enumerate(encabezado):
        celda = tabla.cell(0, j)
        celda.text = texto
    for i, fila in enumerate(filas, start=1):
        for j, texto in enumerate(fila):
            tabla.cell(i, j).text = texto
    for fila in tabla.rows:
        for celda in fila.cells:
            for parrafo in celda.text_frame.paragraphs:
                for run in parrafo.runs:
                    run.font.size = Pt(tamano)
    return slide


def construir():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # 1. Título en español
    diapositiva_portada(
        prs,
        "Sistema de préstamo de herramientas con autómatas y visión artificial",
        [
            "Autor(es): [Nombre del autor / autores]",
            "Modalidad: [Pasantía / Proyecto aplicado / Investigación]",
            "Semestre académico: [2026-2]",
        ],
    )

    # 2. Título en inglés
    diapositiva_portada(
        prs,
        "Tool lending system based on finite automata and computer vision",
        [
            "Author(s): [Author name(s)]",
            "Academic term: [2026-2]",
        ],
    )

    # 3. Generalidades
    diapositiva_texto(prs, "Generalidades del proyecto", [
        (0, "Resumen: se propone un sistema de préstamo de herramientas para un laboratorio, basado en dos autómatas finitos: uno administra el inventario y otro controla la operación física. Una cámara con un modelo YOLO11n-cls verifica visualmente la herramienta antes de autorizar cada transición, y SQLite conserva préstamos e historial. El prototipo se valida con un martillo, puerta y sensores simulados, un portal web local y un monitor sincronizado en tablet."),
        (0, "Palabras clave: autómatas finitos, visión artificial, préstamo de herramientas, YOLO, sistemas embebidos, verificación visual."),
        (0, "Abstract: we propose a tool-lending system for a laboratory, built on two finite automata: one manages the inventory and the other controls the physical operation. A camera with a YOLO11n-cls classification model visually verifies the tool before authorizing each transition, while SQLite stores loans and history. The prototype is validated with one hammer, simulated door and sensors, a local web portal and a synchronized tablet monitor."),
        (0, "Keywords: finite automata, computer vision, tool lending, YOLO, embedded systems, visual verification."),
    ], tamano=13)

    # 4. Problema de investigación (inglés)
    diapositiva_texto(prs, "Research Problem", [
        (0, "In a laboratory there is no reliable record of who takes a tool, simultaneous loans of the same unit are possible, and returns are not verified."),
        (0, "Manual control depends on memory and trust, which leads to losses and unavailable tools."),
        (0, "Research question: how to guarantee that each loan and return is authorized, unique and visually verified, using a deterministic control model (finite automata) combined with real-time computer vision, before investing in the physical cabinet hardware."),
    ], tamano=18)

    # 5. Justificación
    diapositiva_texto(prs, "Justificación", [
        (0, "Técnica: un autómata finito determinista elimina ambigüedad en las transiciones; cada evento inválido se rechaza y se registra, y la verificación visual exige evidencia nueva tras cada operación."),
        (0, "Práctica: reduce pérdidas y préstamos simultáneos sin vigilancia permanente; una restricción única en SQLite impide dos préstamos activos del mismo martillo."),
        (0, "Académica: aplica de forma medible la teoría de autómatas y lenguajes regulares (AFD reconocedor de trazas válidas) junto con visión artificial en un caso real."),
        (0, "Económica: funciona con hardware de bajo costo (computador, celular como cámara) y sin internet una vez instalado; la maqueta física solo se construye tras validar el software."),
    ], tamano=16)

    # 6. Marco teórico o conceptual
    diapositiva_texto(prs, "Marco Teórico o Conceptual", [
        (0, "Autómatas finitos deterministas (AFD): el inventario se modela como M = (Q, Σ, δ, q₀, F) con Q = {Disponible, Reservada, Prestada, En revisión, Fuera de servicio} y Σ = {solicitud_verificada, retiro_verificado, cancelacion_verificada, devolucion_verificada, aprobacion, dano, reparacion}."),
        (0, "Lenguajes regulares: un AFD reconocedor con estado de Error acepta las trazas que terminan en Disponible, lo que permite validar ciclos completos de préstamo."),
        (0, "Máquinas de estados con salidas: el controlador de operación (Inactiva → Abriendo → Esperando retiro/depósito → Cerrando → Verificando → Completada) actúa como transductor con entradas discretizadas de puerta, presencia y evidencia visual."),
        (0, "Visión artificial: clasificación de imágenes con YOLO11n-cls ajustado a cinco clases propias (martillo, destornillador, alicate, vacío, otros), con estabilidad temporal (umbral 0,85, ≥ 5 observaciones, ≥ 2 s)."),
    ], tamano=14)

    # 7. Marco contextual
    diapositiva_texto(prs, "Marco Contextual", [
        (0, "Área de intervención: laboratorio de herramientas de la institución [nombre de la institución], donde estudiantes y docentes retiran herramientas menores."),
        (0, "Descripción institucional: el control actual es manual; no existe registro confiable de quién retira cada herramienta ni verificación de devoluciones."),
        (0, "Alcance del prototipo: una unidad de martillo, escena controlada con cámara (celular por DroidCam o webcam), computador local como servidor y tablet como monitor de solo lectura."),
        (0, "[Insertar mapa/localización del laboratorio y fotografía del contexto]"),
    ], tamano=16)

    # 8. Marco normativo
    diapositiva_texto(prs, "Marco Normativo", [
        (0, "Normas generales aplicables: [reglamento interno del laboratorio; políticas de préstamo de equipos de la institución]."),
        (0, "Normas técnicas y sectoriales: [RETIE si se incorpora electrónica de la puerta; NSR-10 si se construye la maqueta; buenas prácticas de seguridad eléctrica de baja tensión]."),
        (0, "Tratamiento de datos: las imágenes se capturan localmente, sin captura automática de rostros ni subida a servicios externos, conforme a principios de minimización de datos personales."),
        (0, "ODS relacionados: ODS 4 (educación de calidad), ODS 9 (industria, innovación e infraestructura), ODS 12 (producción y consumo responsables)."),
    ], tamano=15)

    # 9. Objetivos
    diapositiva_texto(prs, "Objetivos", [
        (0, "Objetivo general: diseñar e implementar un prototipo de sistema de préstamo de herramientas basado en autómatas finitos y visión artificial, que autorice, registre y verifique cada retiro y devolución en un laboratorio."),
        (0, "Objetivos específicos:"),
        (1, "Modelar el inventario y la operación física como autómatas finitos deterministas con trazas de validación."),
        (1, "Implementar el controlador, la persistencia en SQLite y el portal web con monitor sincronizado."),
        (1, "Construir un dataset propio de cinco clases y ajustar un modelo YOLO11n-cls con evaluación documentada."),
        (1, "Validar el sistema con diez ciclos completos de préstamo/devolución con cámara real."),
    ], tamano=15)

    # 10. Metodología
    diapositiva_tabla(
        prs,
        "Metodología",
        ["Fase", "Actividades", "Productos"],
        [
            ["1. Modelado", "Definir estados, alfabeto y transiciones; AFD reconocedor", "Tablas de transición, app/automata.py"],
            ["2. Implementación", "Motor, persistencia, portal, monitor, simulador", "Software funcional + 47 pruebas aprobadas"],
            ["3. Visión", "Captura de dataset (100 imágenes/clase), entrenamiento, evaluación", "models/herramientas.pt, matriz de confusión"],
            ["4. Validación", "Diez ciclos reales, métricas de latencia y exactitud", "Informe de validación con datos reales"],
            ["5. Documentación", "Informe técnico y presentación", "Documento de trabajo de grado"],
        ],
        tamano=13,
    )

    # 11. Cronograma
    diapositiva_tabla(
        prs,
        "Cronograma",
        ["Actividad", "M1", "M2", "M3", "M4", "M5", "M6"],
        [
            ["Modelado de autómatas", "█", "", "", "", "", ""],
            ["Implementación del prototipo", "█", "█", "", "", "", ""],
            ["Dataset y entrenamiento del modelo", "", "", "█", "█", "", ""],
            ["Validación con ciclos reales", "", "", "", "█", "█", ""],
            ["Redacción y sustentación", "", "", "", "", "█", "█"],
        ],
        tamano=13,
    )

    # 12. Resultados esperados (inglés)
    diapositiva_texto(prs, "Expected Results", [
        (0, "A working prototype that authorizes, records and verifies every loan and return, rejecting invalid events deterministically."),
        (0, "A custom image dataset (five classes, ~100 images per class) and a fine-tuned YOLO11n-cls model with documented confusion matrix, accuracy and false positives."),
        (0, "Measured results from ten complete loan/return cycles with the real camera, including latency and visual evidence."),
        (0, "An academic validation of finite automata and regular languages applied to access control: accepted traces correspond to complete, correct lending cycles."),
        (0, "A validated software base ready for the next milestone: the physical cabinet with real door and presence sensors."),
    ], tamano=15)

    # 13. Bibliografía
    diapositiva_texto(prs, "Bibliografía", [
        (0, "1. Hopcroft, J. E., Motwani, R. y Ullman, J. D. (2007). Introduction to Automata Theory, Languages, and Computation (3.ª ed.). Pearson."),
        (0, "2. Sipser, M. (2013). Introduction to the Theory of Computation (3.ª ed.). Cengage Learning."),
        (0, "3. Redmon, J. y Farhadi, A. (2018). YOLOv3: An Incremental Improvement. arXiv:1804.02767."),
        (0, "4. Ultralytics (2024). YOLO11 Documentation. https://docs.ultralytics.com/models/yolo11/"),
        (0, "5. Ultralytics (2024). Image Classification Tasks. https://docs.ultralytics.com/tasks/classify/"),
        (0, "6. Ultralytics (2024). Classification Datasets. https://docs.ultralytics.com/datasets/classify/"),
        (0, "7. Pallets Projects (2024). Flask: Deploying with Waitress. https://flask.palletsprojects.com/en/stable/deploying/waitress/"),
        (0, "8. Jocher, G. et al. (2023). Ultralytics YOLOv8. Zenodo. https://doi.org/10.5281/zenodo.7347926"),
        (0, "9. Dev47Apps (2024). DroidCam User Guide. https://droidcam.app/help/"),
        (0, "10. Bradski, G. (2000). The OpenCV Library. Dr. Dobb's Journal of Software Tools."),
    ], tamano=12)

    prs.save(SALIDA)
    print(f"Guardado: {SALIDA}")


if __name__ == "__main__":
    construir()
