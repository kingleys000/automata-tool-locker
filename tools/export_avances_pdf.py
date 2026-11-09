"""Exporta los avances Markdown a PDF carta en blanco y negro usando LibreOffice."""
from __future__ import annotations

import base64
import html
import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf"
ADVANCES = {
    "AVANCE3_METODOLOGIA": (ROOT / "docs" / "AVANCE3_METODOLOGIA.md", "Avance 3", "Metodología"),
    "AVANCE4_ANALISIS": (ROOT / "docs" / "AVANCE4_ANALISIS.md", "Avance 4", "Análisis del problema"),
    "AVANCE5_DISENO": (ROOT / "docs" / "AVANCE5_DISENO.md", "Avance 5", "Diseño de la solución"),
}


def inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"\$([^$]+)\$", r"<code>\1</code>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"<span class='link'>\1</span>", text)
    return text


def table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def image_data(src: str, temp_dir: Path) -> str | None:
    path = (ROOT / "docs" / src).resolve()
    if not path.exists():
        path = (ROOT / src).resolve()
    if not path.is_file() or path.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
        return None
    gray = ImageOps.grayscale(Image.open(path).convert("RGB"))
    gray.thumbnail((1600, 1100))
    converted = temp_dir / f"{path.stem}-bw.png"
    gray.save(converted, optimize=True)
    return "data:image/png;base64," + base64.b64encode(converted.read_bytes()).decode("ascii")


def markdown_body(source: Path, temp_dir: Path) -> str:
    lines = source.read_text("utf-8").splitlines()
    out: list[str] = []
    i = 0
    in_ul = in_ol = in_code = False
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("```"):
            if stripped.lower().startswith("```mermaid"):
                out.append("<p class='diagram-note'>Diagrama editable disponible en la carpeta <code>docs/avances/diagramas</code>.</p>")
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    i += 1
                i += 1
                continue
            if not in_code:
                if in_ul: out.append("</ul>"); in_ul = False
                if in_ol: out.append("</ol>"); in_ol = False
                out.append("<pre><code>"); in_code = True
            else:
                out.append("</code></pre>"); in_code = False
            i += 1
            continue
        if in_code:
            out.append(html.escape(line))
            i += 1
            continue
        if stripped.startswith("!["):
            m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", stripped)
            if m:
                uri = image_data(m.group(2), temp_dir)
                if uri:
                    out.append(f"<figure><img src='{uri}'/><figcaption>{inline(m.group(1))}</figcaption></figure>")
                else:
                    out.append(f"<p class='diagram-note'>{inline(m.group(1))}</p>")
            i += 1
            continue
        if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"\s*\|?\s*:?-{3,}", lines[i + 1]):
            headers = table_cells(stripped)
            i += 2
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = table_cells(lines[i])
                rows.append((cells + [""] * len(headers))[:len(headers)])
                i += 1
            if len(headers) > 4:
                # Apilar tablas muy anchas como ficha por registro para conservar
                # legibilidad en página vertical sin quitar información.
                for cells in rows:
                    out.append("<table class='stacked'><tbody>")
                    out.append(f"<tr><th colspan='2'>{inline(headers[0])}: {inline(cells[0])}</th></tr>")
                    for header, value in zip(headers[1:], cells[1:]):
                        out.append(f"<tr><th>{inline(header)}</th><td>{inline(value)}</td></tr>")
                    out.append("</tbody></table>")
            else:
                out.append("<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in headers) + "</tr></thead><tbody>")
                for cells in rows:
                    out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
                out.append("</tbody></table>")
            continue
        if stripped.startswith("### ") or stripped.startswith("## ") or stripped.startswith("# "):
            if in_ul: out.append("</ul>"); in_ul = False
            if in_ol: out.append("</ol>"); in_ol = False
            level = len(stripped) - len(stripped.lstrip("#"))
            title = stripped[level:].strip()
            out.append(f"<h{min(level+1,4)}>{inline(title)}</h{min(level+1,4)}>")
            i += 1
            continue
        if stripped.startswith(">"):
            if in_ul: out.append("</ul>"); in_ul = False
            if in_ol: out.append("</ol>"); in_ol = False
            quote = stripped.lstrip(">").strip()
            if quote:
                out.append(f"<blockquote>{inline(quote)}</blockquote>")
            i += 1
            continue
        if re.match(r"^\s*[-*] ", line):
            if in_ol: out.append("</ol>"); in_ol = False
            if not in_ul: out.append("<ul>"); in_ul = True
            out.append(f"<li>{inline(re.sub(r'^\s*[-*] ', '', line))}</li>")
            i += 1
            continue
        if re.match(r"^\s*\d+\. ", line):
            if in_ul: out.append("</ul>"); in_ul = False
            if not in_ol: out.append("<ol>"); in_ol = True
            out.append(f"<li>{inline(re.sub(r'^\s*\d+\. ', '', line))}</li>")
            i += 1
            continue
        if in_ul: out.append("</ul>"); in_ul = False
        if in_ol: out.append("</ol>"); in_ol = False
        if stripped == "---":
            out.append("<hr/>")
        elif stripped:
            out.append(f"<p>{inline(stripped)}</p>")
        i += 1
    if in_ul: out.append("</ul>")
    if in_ol: out.append("</ol>")
    if in_code: out.append("</code></pre>")
    return "\n".join(out)


CSS = """
@page { size: letter; margin: 0.78in 0.72in 0.72in 0.72in; }
body { font-family: 'Times New Roman', 'Liberation Serif', serif; color:#000; background:#fff; font-size:10pt; line-height:1.16; }
h1 { font-size:17pt; text-align:center; margin:16pt 0 7pt; font-weight:bold; }
h2 { font-size:13pt; text-align:center; margin:14pt 0 7pt; font-weight:bold; }
h3 { font-size:11pt; margin:11pt 0 5pt; font-weight:bold; }
h4 { font-size:10pt; margin:8pt 0 4pt; font-weight:bold; }
p { text-align:justify; margin:4pt 0 6pt; orphans:2; widows:2; }
li { margin:2pt 0; text-align:justify; }
table { width:100%; border-collapse:collapse; margin:7pt 0 10pt; font-size:8.6pt; table-layout:auto; }
th,td { border:0.55pt solid #000; padding:3pt 4pt; vertical-align:top; }
th { font-weight:bold; text-align:center; background:#fff; }
.stacked { font-size:8.4pt; margin:5pt 0 7pt; }
.stacked th:first-child { width:25%; }
tr { page-break-inside:avoid; }
thead { display:table-header-group; }
blockquote { border-left:1pt solid #000; margin:8pt 10pt; padding-left:8pt; font-style:italic; }
pre { white-space:pre-wrap; word-wrap:break-word; border:0.5pt solid #000; padding:6pt; font-size:8pt; line-height:1.05; font-family:'Liberation Mono',monospace; }
code { font-family:'Liberation Mono',monospace; font-size:0.92em; }
hr { border:0; border-top:0.7pt solid #000; margin:8pt 0; }
figure { margin:10pt auto; text-align:center; page-break-inside:avoid; }
figure img { max-width:6.6in; max-height:5.8in; }
figcaption { font-size:9pt; font-style:italic; margin-top:3pt; }
.cover { page-break-after:always; height:9in; box-sizing:border-box; padding-top:1.45in; text-align:center; }
.cover h1 { font-size:22pt; }
.cover p { text-align:center; font-size:12pt; }
.cover .cover-meta { margin-top:22pt; line-height:1.35; font-size:12pt; }
.cover .cover-meta p { margin:5pt 0; text-align:center; }
.page-break { page-break-before:always; break-before:page; height:0; }
.diagram-note { font-style:italic; text-align:left; font-size:9pt; }
.link { text-decoration:underline; }
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="avances-pdf-") as td:
        temp_dir = Path(td)
        html_files = []
        for stem, (source, avance, title) in ADVANCES.items():
            content = markdown_body(source, temp_dir)
            page = f"""<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style><title>{avance} {title}</title></head><body>
<div class='cover'><center><p>PROYECTO DE AULA · TEORÍA DE LA COMPUTACIÓN</p><h1>{avance}<br/>{title}</h1><p>Sistema de préstamo de herramientas basado en autómatas finitos y verificación visual</p><p>Documento de trabajo académico</p><div class='cover-meta'><p><strong>Juan Diego Torres Mola</strong></p><p>Ingeniería de Sistemas</p><p>Universidad de Pamplona</p><p>Docente: Mercy Lucero Gómez Rincón</p><p>Cúcuta, Norte de Santander</p></div></center></div><p class='page-break'>&nbsp;</p>
{content}</body></html>"""
            html_path = temp_dir / f"{stem}.html"
            html_path.write_text(page, encoding="utf-8")
            html_files.append(html_path)
        subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", str(OUT), *map(str, html_files)], check=True)
        for html_file in html_files:
            pdf = OUT / f"{html_file.stem}.pdf"
            if not pdf.exists() or pdf.stat().st_size < 10_000:
                raise RuntimeError(f"PDF ausente o truncado: {pdf}")
            print(pdf)


if __name__ == "__main__":
    main()
