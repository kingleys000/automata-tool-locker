"""Exporta figuras técnicas desde las definiciones reales del proyecto; requiere Graphviz."""
import json
from pathlib import Path
import runpy
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'avances' / 'figuras'
OUT.mkdir(parents=True, exist_ok=True)
def q(value):
    return json.dumps(value, ensure_ascii=False)
def render(name, body):
    text = 'digraph G {\ngraph [rankdir=LR, bgcolor="white", pad=0.3, nodesep=0.4, ranksep=0.7];\nnode [shape=box, style="rounded", fontname="DejaVu Sans", fontsize=12];\nedge [fontname="DejaVu Sans", fontsize=10];\n' + body + '\n}\n'
    path = OUT / (name + '.dot')
    path.write_text(text, encoding='utf-8')
    for fmt in ('svg', 'png'):
        subprocess.run(['dot', '-T'+fmt, str(path), '-o', str(OUT/(name+'.'+fmt))], check=True)

definitions = runpy.run_path(str(ROOT/'app/automata.py'))['DEFINITIONS']
for name, machine in definitions.items():
    body = ['inicio [shape=point];', f'inicio -> {q(machine["initial"])};']
    for edge in machine['transitions']:
        body.append(f'{q(edge["from"])} -> {q(edge["to"])} [label={q(edge["event"])}];')
    render('automata_'+name, '\n'.join(body))
render('arquitectura', '''control [label="Navegador local\\n/control"];
monitor [label="Monitor de lectura\\n/monitor"];
web [label="Flask\\nAPI y vistas"];
motor [label="Motor\\nReglas y autómatas"];
camara [label="Cámara\\nCaptura y clasificación"];
hardware [label="Adaptador simulado\\nPuerta y presencia"];
db [shape=cylinder, label="SQLite\\nEstado y registros"];
control -> web [label="acciones y consultas"];
monitor -> web [label="consultas"];
web -> motor;
camara -> motor [label="observaciones"];
hardware -> motor [label="señales"];
motor -> hardware [label="comandos"];
motor -> db [label="transacciones"];
''')
render('modelo_datos', '''users [label="users\\ncode PK\\nname\\nrole"];
loans [label="loans\\nid PK\\nuser_code\\ntool\\nborrowed_at\\nreturned_at\\nsimulated_hardware"];
events [label="events\\nseq PK\\ntime, machine, event\\nprevious, current, source\\naccepted, message"];
state [label="state\\nid PK (id=1)\\nvalue JSON"];
requests [label="requests\\nid PK\\npayload\\nresult"];
users -> loans [style=dashed, label="1 a muchos\\nRelación lógica; sin FK declarada"];
''')
print('Figuras exportadas a', OUT)
