"use strict";

const $ = id => document.getElementById(id);
const control = document.body.dataset.view === "control";
const token = document.querySelector('meta[name="simulation-token"]').content;
const ns = "http://www.w3.org/2000/svg";
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
const layouts = {
  inventario: {"Disponible":[120,100],"Reservada":[380,100],"Prestada":[640,100],"En revisión":[640,340],"Fuera de servicio":[280,340]},
  operacion: {"Inactiva":[115,65],"Abriendo":[115,210],"Esperando retiro":[380,120],"Esperando depósito":[380,285],"Cerrando":[645,200],"Verificando":[645,365],"Completada":[380,465],"Incidencia":[115,465]}
};
const objectNames = {martillo:"Martillo",vacio:"Vacío",alicate:"Alicate",destornillador:"Destornillador"};
const graphViews = new Map();
let snapshot, online = false, busy = false, lastRevision = -1, toastTimer, pending;
let angle = -28;

function svgElement(tag, attrs = {}, value = "") {
  const node = document.createElementNS(ns, tag);
  for (const [key, val] of Object.entries(attrs)) node.setAttribute(key, val);
  if (value) node.textContent = value;
  return node;
}
function textNode(tag, text, className) {
  const node = document.createElement(tag);
  node.textContent = text;
  if (className) node.className = className;
  return node;
}
function drawGraph(machine, definition) {
  const svg = svgElement("svg", {viewBox:"0 0 760 520",class:"automaton",role:"img","aria-label":definition.title});
  const defs = svgElement("defs");
  for (const [name, color] of [["normal", "#adc5b4"], ["latest", "#d88747"]]) {
    const marker = svgElement("marker", {id:`${machine}-${name}`,viewBox:"0 0 10 10",refX:9,refY:5,markerWidth:6,markerHeight:6,orient:"auto-start-reverse"});
    marker.append(svgElement("path", {d:"M 0 0 L 10 5 L 0 10 z",fill:color}));
    defs.append(marker);
  }
  svg.append(defs);
  const edges = definition.transitions.map((edge, index) => {
    const [x1,y1] = layouts[machine][edge.from], [x2,y2] = layouts[machine][edge.to];
    const dx = x2-x1, dy = y2-y1, scale = Math.max(Math.abs(dx)/86, Math.abs(dy)/27);
    let sx = x1+dx/scale, sy = y1+dy/scale, ex = x2-dx/scale, ey = y2-dy/scale;
    let tx=(sx+ex)/2, ty=(sy+ey)/2-9, d;
    const failure = edge.event === "fallo" || edge.from === "Incidencia";
    if (machine === "inventario" && edge.event === "cancelacion_verificada") {
      sx=x1; sy=y1-27; ex=x2; ey=y2-27;
      d=`M ${sx} ${sy} Q ${(sx+ex)/2} -15 ${ex} ${ey}`; tx=(sx+ex)/2; ty=24;
    } else if (machine === "inventario" && edge.event === "reparacion") {
      sx=x1; sy=y1+27; ex=x2; ey=y2+27;
      d=`M ${sx} ${sy} Q ${(sx+ex)/2} 465 ${ex} ${ey}`; tx=(sx+ex)/2; ty=429;
    } else if (failure) {
      const mx=(sx+ex)/2+(edge.from === "Incidencia" ? -35 : 27), my=(sy+ey)/2;
      d=`M ${sx} ${sy} Q ${mx} ${my} ${ex} ${ey}`; tx=mx; ty=my+(index%2?9:-9);
    } else d=`M ${sx} ${sy} L ${ex} ${ey}`;
    const group = svgElement("g", {"data-edge":index});
    const path = svgElement("path", {d,class:"edge"+(failure?" failure":""),"marker-end":`url(#${machine}-normal)`});
    path.append(svgElement("title", {}, `e${index+1}: ${edge.from} + ${edge.label} → ${edge.to}`));
    const label = svgElement("text", {x:tx,y:ty,"text-anchor":"middle",class:"edge-label"}, "e"+(index+1));
    label.append(svgElement("title", {}, edge.label));
    group.append(path,label); svg.append(group);
    return {path,label,definition:edge,failure};
  });
  const initial=layouts[machine][definition.initial];
  svg.append(svgElement("path", {d:`M ${initial[0]-109} ${initial[1]} L ${initial[0]-87} ${initial[1]}`,class:"initial-arrow","marker-end":`url(#${machine}-normal)`}));
  const nodes = new Map();
  for (const state of definition.states) {
    const [x,y] = layouts[machine][state];
    const group=svgElement("g", {class:"graph-node"+(state==="Incidencia"?" incident":""),"data-state":state});
    group.append(svgElement("rect", {x:x-85,y:y-26,width:170,height:52,rx:11}));
    group.append(svgElement("text", {x,y:y+5,"text-anchor":"middle"}, state));
    group.append(svgElement("text", {x,y:y+43,"text-anchor":"middle",class:"current-label"}, "ESTADO ACTUAL"));
    svg.append(group); nodes.set(state,group);
  }
  const dot=svgElement("circle", {r:6,class:"edge-dot"}); svg.append(dot);
  $("graph-"+machine).replaceChildren(svg);
  graphViews.set(machine, {edges,nodes,dot,lastSeq:null,current:null,animation:null});
}
function animateEdge(view, path) {
  if (view.animation) cancelAnimationFrame(view.animation);
  if (reducedMotion.matches) return;
  const length=path.getTotalLength(), started=performance.now();
  function frame(now) {
    const t=Math.min((now-started)/650,1), point=path.getPointAtLength(length*t);
    view.dot.setAttribute("cx",point.x);view.dot.setAttribute("cy",point.y);
    view.dot.style.opacity=t<1?"1":"0";
    if(t<1) view.animation=requestAnimationFrame(frame);
  }
  view.animation=requestAnimationFrame(frame);
}
function updateGraph(machine, state, last, definition) {
  if (!graphViews.has(machine)) drawGraph(machine,definition);
  const view=graphViews.get(machine);
  if (view.current !== state) {
    for(const [name,node] of view.nodes) {
      node.classList.toggle("active",name===state);
      node.classList.toggle("changed",name===state && view.current!==null);
    }
    view.current=state;
  }
  const seq=last?.seq??0;
  if (view.lastSeq===seq) return;
  view.lastSeq=seq;
  let selected=-1;
  view.edges.forEach((item,index)=>{
    const active=Boolean(last && item.definition.from===last.previous && item.definition.event===last.event);
    item.path.classList.toggle("latest",active); item.label.classList.toggle("latest",active);
    item.path.setAttribute("marker-end",`url(#${machine}-${active?"latest":"normal"})`);
    if(active) selected=index;
  });
  const caption=$("caption-"+machine); caption.replaceChildren();
  if (last && selected>=0) {
    caption.append(textNode("span","e"+(selected+1),"event-symbol"),textNode("strong",`${last.previous} → ${last.current}`),textNode("span",view.edges[selected].definition.label));
    animateEdge(view,view.edges[selected].path);
  } else caption.textContent=`Estado inicial: ${state}.`;
}
function updateScene(s) {
  const opening = !s.door_closed && s.operation!=="Cerrando";
  $("door").classList.toggle("open",opening);
  $("tool").classList.toggle("outside",s.object!=="martillo" && (s.loan_active || s.mode==="prestamo"));
  $("tool").classList.toggle("absent",s.object!=="martillo" && !s.loan_active && s.mode!=="prestamo");
  $("wrong-tool").hidden=!(["alicate","destornillador"].includes(s.object));
  $("wrong-tool").classList.toggle("screwdriver",s.object==="destornillador");
  $("wrong-label").textContent=objectNames[s.object]?.toUpperCase()||"";
  $("door-value").textContent=s.operation==="Cerrando"?"Cerrando…":s.door_closed?"Cerrada":"Abierta";
  $("object-value").textContent=objectNames[s.object];
  $("sensor-value").textContent=s.sensor_connected?"Conectado":"Desconectado";
  $("door-dot").classList.toggle("off",!s.door_closed);
  $("object-dot").classList.toggle("off",s.object==="vacio");
  $("sensor-dot").classList.toggle("error",!s.sensor_connected);
  $("scene-led").textContent=s.operation==="Incidencia"?"Incidencia":s.inventory;
  $("scene-led").classList.toggle("incident",s.operation==="Incidencia");
  $("cabinet-light").className=s.operation==="Incidencia"||s.inventory==="Fuera de servicio"?"red":s.operation!=="Inactiva"?"green":"";
  $("scene").setAttribute("aria-label",`Compartimiento 3D: puerta ${s.door_closed?"cerrada":"abierta"}, contenido ${objectNames[s.object]}, inventario ${s.inventory}.`);
}
function updateControls() {
  if(!control || !snapshot) return;
  const d=snapshot.demo, playing=d?.status==="playing", paused=d?.status==="paused", disabled=!online||busy;
  $("play").disabled=disabled;
  $("pause").disabled=disabled||!(playing||paused);
  $("pause").textContent=paused?"▶ Continuar":"Ⅱ Pausar";
  $("step").disabled=disabled||playing;
  $("reset").disabled=disabled;
  $("speed").disabled=disabled;
  $("scenario").disabled=disabled;
  document.querySelectorAll("[data-command],#deposit,#sensor-toggle").forEach(el=>el.disabled=disabled||playing||paused);
  $("sensor-toggle").textContent=snapshot.state.sensor_connected?"Desconectar sensor":"Reconectar sensor";
  $("next-kicker").textContent=playing?"SIGUIENTE EN LA REPRODUCCIÓN":paused?"DEMOSTRACIÓN PAUSADA":"SIGUIENTE ACCIÓN";
  $("next-label").textContent=snapshot.next_label;
  $("demo-progress").textContent=d?`${d.status==="finished"?"Completado":paused?"Pausa":"Paso"} · ${d.index}/${d.total}`:"Modo libre";
  if(document.activeElement!==$("speed")) $("speed").value=String(snapshot.speed);
}
function renderHistory(data) {
  const host=$("history"); host.replaceChildren();
  for(const row of data.events.slice(-30).reverse()) {
    const li=document.createElement("li");if(!row.accepted)li.className="rejected";
    const content=document.createElement("div");
    content.append(textNode("strong",row.machine?`${row.previous} → ${row.current}`:row.accepted?row.event.replaceAll("_"," "):"Acción rechazada"),textNode("small",row.message));
    li.append(textNode("span",String(row.seq).padStart(3,"0"),"event-index"),content);host.append(li);
  }
  $("loan-count").textContent=`${data.state.loan_count} préstamos · ${data.state.returned_count} devoluciones`;
}
function render(data) {
  snapshot=data;
  const s=data.state;
  $("inventory-state").textContent=s.inventory;$("operation-state").textContent=s.operation;
  $("inventory-state").classList.toggle("incident",s.inventory==="Fuera de servicio");
  $("operation-state").classList.toggle("incident",s.operation==="Incidencia");
  for(const [machine,state] of [["inventario",s.inventory],["operacion",s.operation]]) updateGraph(machine,state,data.last_transitions[machine],data.definitions[machine]);
  $("message").textContent=s.message;
  $("event-number").textContent="EVENTO "+String(data.revision).padStart(3,"0");
  $("explanation").classList.toggle("rejected",data.events.at(-1)?.accepted===false);
  if(control) {
    updateScene(s);updateControls();
    if(lastRevision!==data.revision)renderHistory(data);
  }
  lastRevision=data.revision;
}
async function poll() {
  let delay=250;
  try {
    const response=await fetch("/api/simulacion/estado",{cache:"no-store",signal:AbortSignal.timeout(3500)});
    if(!response.ok)throw new Error("Sin respuesta");
    const data=await response.json();online=true;
    $("connection").textContent="Sincronizado";$("connection").classList.remove("lost");$("offline").hidden=true;
    render(data);
  } catch {
    online=false;$("connection").textContent="Desconectado";$("connection").classList.add("lost");$("offline").hidden=false;
    updateControls();delay=1200;
  } finally {setTimeout(poll,delay);}
}
function toast(message,error=false) {
  if(!control)return;
  clearTimeout(toastTimer);$("toast").textContent=message;$("toast").className="toast"+(error?" error":"");$("toast").hidden=false;
  toastTimer=setTimeout(()=>$("toast").hidden=true,5500);
}
async function send(action,payload={}) {
  if(!online||busy)return;
  busy=true;updateControls();
  const signature=JSON.stringify([action,payload]);
  const envelope=pending?.signature===signature?pending.envelope:{action,payload,id:crypto.randomUUID()};
  pending={signature,envelope};
  try {
    const response=await fetch("/api/simulacion/acciones",{method:"POST",headers:{"Content-Type":"application/json","X-Simulation-Token":token},body:JSON.stringify(envelope),signal:AbortSignal.timeout(5000)});
    const result=await response.json();pending=null;
    if(!result.ok)toast(result.message,true);
  } catch {toast("No se pudo confirmar la acción. Al repetirla se reutiliza el identificador para evitar duplicados.",true);}
  finally {busy=false;updateControls();}
}
if(control) {
  $("play").addEventListener("click",()=>send("demostrar",{scenario:$("scenario").value}));
  $("pause").addEventListener("click",()=>send(snapshot.demo?.status==="paused"?"continuar":"pausar"));
  $("step").addEventListener("click",()=>send("paso"));
  $("reset").addEventListener("click",()=>send("reiniciar"));
  $("speed").addEventListener("change",()=>send("velocidad",{seconds:Number($("speed").value)}));
  $("scenario").addEventListener("change",()=>{$("scenario-description").textContent=snapshot?.scenarios[$("scenario").value]?.description||"";});
  document.querySelectorAll("[data-command]").forEach(button=>button.addEventListener("click",()=>send(button.dataset.command)));
  $("sensor-toggle").addEventListener("click",()=>send(snapshot.state.sensor_connected?"desconectar":"conectar"));
  $("deposit").addEventListener("click",()=>send("depositar",{object:$("deposit-object").value}));
  function rotateWorld(delta) {
    angle=delta===null?-28:Math.max(-60,Math.min(40,angle+delta));
    const scale=innerWidth<=600?.78:innerWidth<=1150?.9:1;
    $("world").style.transform=`translate(-50%,-50%) rotateX(-12deg) rotateY(${angle}deg) scale(${scale})`;
  }
  $("view-left").addEventListener("click",()=>rotateWorld(-12));
  $("view-right").addEventListener("click",()=>rotateWorld(12));
  $("view-reset").addEventListener("click",()=>rotateWorld(null));
  addEventListener("resize",()=>rotateWorld(0));
  fetch("/api/simulacion/conexion").then(r=>r.json()).then(data=>{
    $("tablet-links").replaceChildren();
    for(const url of data.urls){const a=textNode("a",url);a.href=url;a.target="_blank";a.rel="noopener";$("tablet-links").append(a);}
    if(!data.urls.length)$("tablet-links").textContent="Consulta tu IPv4 con ipconfig y abre /automatas en este puerto.";
  }).catch(()=>{$("tablet-links").textContent="Consulta la IPv4 del computador con ipconfig.";});
}
if($("fullscreen"))$("fullscreen").addEventListener("click",async()=>{
  try {if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}
  catch {$("fullscreen").textContent="Usa pantalla completa del navegador";}
});
poll();
