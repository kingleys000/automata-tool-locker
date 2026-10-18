"use strict";
const $ = id => document.getElementById(id);
const mode = document.body.dataset.mode;
const token = document.querySelector('meta[name="control-token"]').content;
const labels = {martillo:"Martillo",destornillador:"Destornillador",alicate:"Alicate",vacio:"Vacío",otros:"Otro objeto"};
let cursor = 0, snapshot = null, online = false, busy = false, toastTimer, pendingAction = null;
const history = new Map();
const svgNS = "http://www.w3.org/2000/svg";
const layouts = {
  inventario: {"Disponible":[120,90],"Reservada":[370,90],"Prestada":[620,90],"En revisión":[620,315],"Fuera de servicio":[280,315]},
  operacion: {"Inactiva":[105,65],"Abriendo":[105,205],"Esperando retiro":[340,115],"Esperando depósito":[340,280],"Cerrando":[600,200],"Verificando":[600,350],"Completada":[340,465],"Incidencia":[105,465]}
};
function element(tag, attrs={}, text="") { const node=document.createElementNS(svgNS,tag); for(const [key,value] of Object.entries(attrs))node.setAttribute(key,value);if(text)node.textContent=text;return node; }
function textNode(tag, text, className="") {const el=document.createElement(tag);el.textContent=text;if(className)el.className=className;return el;}
function toast(message, error=false, persistent=false){clearTimeout(toastTimer);$("toast").textContent=message;$("toast").className="toast"+(error?" error":"");$("toast").hidden=false;if(!persistent)toastTimer=setTimeout(()=>$("toast").hidden=true,6500);}
function timeText(value){return new Date(value).toLocaleTimeString("es-CO",{timeZone:"America/Bogota",hour:"2-digit",minute:"2-digit",second:"2-digit"});}
function sourceTag(value){return textNode("span",{camara:"CÁMARA REAL",simulador:"SIMULADOR",usuario:"USUARIO",sistema:"SISTEMA"}[value]||value,"source-tag "+value);}

function drawGraph(machine,definition){
 const host=$("graph-"+machine);host.replaceChildren();
 const svg=element("svg",{viewBox:"0 0 740 535",class:"automaton-svg",role:"img","aria-label":definition.title+". El estado actual se indica en el resumen y en el diagrama."});
 const defs=element("defs");for(const [suffix,color] of [["normal","#a8beb2"],["latest","#b65b22"],["failure","#c8b9bd"]]){const marker=element("marker",{id:machine+"-"+suffix,viewBox:"0 0 10 10",refX:9,refY:5,markerWidth:6,markerHeight:6,orient:"auto-start-reverse"});marker.append(element("path",{d:"M 0 0 L 10 5 L 0 10 z",fill:color}));defs.append(marker);}svg.append(defs);
 definition.transitions.forEach((edge,index)=>{
   const [x1,y1]=layouts[machine][edge.from], [x2,y2]=layouts[machine][edge.to];
   const dx=x2-x1,dy=y2-y1,scale=Math.max(Math.abs(dx)/86,Math.abs(dy)/29);
   let sx=x1+dx/scale,sy=y1+dy/scale,ex=x2-dx/scale,ey=y2-dy/scale;
   const failure=edge.event==="fallo"||edge.from==="Incidencia";
   let path,tx=(sx+ex)/2,ty=(sy+ey)/2-8;
   if(machine==="inventario"&&edge.event==="cancelacion_verificada"){
     sx=x1;sy=y1-29;ex=x2;ey=y2-29;path=`M ${sx} ${sy} Q ${(sx+ex)/2} -12 ${ex} ${ey}`;tx=(sx+ex)/2;ty=19;
   }else if(machine==="inventario"&&edge.event==="reparacion"){
     sy=y1+29;ey=y2+29;sx=x1;ex=x2;path=`M ${sx} ${sy} Q ${(sx+ex)/2} 410 ${ex} ${ey}`;tx=(sx+ex)/2;ty=388;
   }else if(failure){
     const bend=edge.from==="Incidencia"?-33:26;const mx=(sx+ex)/2+bend,my=(sy+ey)/2;
     path=`M ${sx} ${sy} Q ${mx} ${my} ${ex} ${ey}`;tx=mx;ty=my+(index%2?8:-8);
   }else path=`M ${sx} ${sy} L ${ex} ${ey}`;
   const group=element("g",{"data-edge":index});const line=element("path",{d:path,class:"graph-edge"+(failure?" failure":""),"marker-end":`url(#${machine}-${failure?"failure":"normal"})`});
   line.append(element("title",{},`${edge.from} + ${edge.label} → ${edge.to}`));group.append(line);
   group.append(element("text",{x:tx,y:ty,"text-anchor":"middle",class:"edge-label"+(failure?" failure":"")},"e"+(index+1)));svg.append(group);
 });
 const initial=layouts[machine][definition.initial];svg.append(element("path",{d:`M ${initial[0]-102} ${initial[1]} L ${initial[0]-86} ${initial[1]}`,class:"start-arrow","marker-end":`url(#${machine}-normal)`}));
 for(const state of definition.states){const [x,y]=layouts[machine][state],g=element("g",{"data-state":state,class:"graph-node"+(state==="Incidencia"?" incident":"")});g.append(element("rect",{x:x-85,y:y-28,width:170,height:56,rx:12}));g.append(element("text",{x,y:y+4,"text-anchor":"middle"},state));g.append(element("text",{x,y:y+46,"text-anchor":"middle",class:"node-current",visibility:"hidden"},"ESTADO ACTUAL"));svg.append(g);}
 host.append(svg);
 const table=document.createElement("table");const head=document.createElement("thead"),tr=document.createElement("tr");for(const title of ["SÍMBOLO","DESDE","EVENTO","HACIA"])tr.append(textNode("th",title));head.append(tr);table.append(head);const body=document.createElement("tbody");definition.transitions.forEach((edge,i)=>{const row=document.createElement("tr");for(const value of ["e"+(i+1),edge.from,edge.label,edge.to])row.append(textNode("td",value));body.append(row);});table.append(body);$("table-"+machine).replaceChildren(table);
}

function updateGraph(machine,current,last){
 const host=$("graph-"+machine);if(!host.querySelector("svg"))drawGraph(machine,snapshot.definitions[machine]);
 host.querySelectorAll("[data-state]").forEach(node=>{const active=node.dataset.state===current;node.classList.toggle("active",active);node.querySelector(".node-current").setAttribute("visibility",active?"visible":"hidden");});
 host.querySelectorAll("[data-edge]").forEach(group=>{const edge=snapshot.definitions[machine].transitions[Number(group.dataset.edge)],active=last&&last.previous===edge.from&&last.event===edge.event;const path=group.querySelector("path");path.classList.toggle("latest",Boolean(active));group.querySelector("text").classList.toggle("latest",Boolean(active));path.setAttribute("marker-end",`url(#${machine}-${active?"latest":path.classList.contains("failure")?"failure":"normal"})`);});
 const caption=$("transition-"+machine);caption.replaceChildren();if(last){caption.append(sourceTag(last.source),textNode("strong",`${last.previous} → ${last.current}`),textNode("div",`${last.event} · ${timeText(last.time)}`));}else caption.append(textNode("span",`Estado inicial: ${current}. Todavía no hay transiciones.`));
}

function updateControls(){
 if(mode!=="control"||!snapshot)return;
 const s=snapshot.state,disabled=!online||busy;
 const available={solicitar:s.operation==="Inactiva"&&s.inventory==="Disponible",devolver:s.operation==="Inactiva"&&s.inventory==="Prestada",cerrar:["Esperando retiro","Esperando depósito"].includes(s.operation),cancelar:s.operation==="Esperando retiro",reintentar:s.operation==="Incidencia",finalizar:s.operation==="Completada",puerta_abierta:s.operation==="Abriendo",puerta_cerrada:s.operation==="Cerrando",aprobar:s.operation==="Inactiva"&&s.inventory==="En revisión",danada:s.operation==="Inactiva"&&s.inventory==="En revisión",reparada:s.operation==="Inactiva"&&s.inventory==="Fuera de servicio"};
 document.querySelectorAll("[data-action]").forEach(button=>button.disabled=disabled||!available[button.dataset.action]);
 $("presence").disabled=disabled||!s.hardware_connected;$("sensor-connected").disabled=disabled;
 $("start-camera").disabled=disabled||snapshot.camera_device.running;$("stop-camera").disabled=disabled||!snapshot.camera_device.running;$("capture-image").disabled=disabled||!snapshot.camera_device.preview_ready;
 $("user-name").textContent=snapshot.users.find(user=>user.code===$("user-code").value.trim())?.name||"Código no registrado";
}

function render(data){
 snapshot=data;$("inventory-state").textContent=data.state.inventory;$("operation-state").textContent=data.state.operation;
 $("operation-mode").textContent=({prestamo:"Préstamo",devolucion:"Devolución",cancelacion:"Cancelación"}[data.state.mode]||"Sin operación activa")+(data.state.owner?" · Usuario "+data.state.owner:"");
 $("recognition-state").textContent=data.camera.stable_label?labels[data.camera.stable_label]:data.camera.fresh?"Verificando…":"Sin evidencia";
 $("recognition-detail").textContent=data.camera.fresh?`${labels[data.camera.label]} · puntuación ${(100*data.camera.confidence).toFixed(0)} %${data.camera.stable_label?" · estable":" · aún no estable"}`:data.camera_device.model_ready?"Cámara sin observaciones recientes":"Modelo o cámara pendientes";
 $("event-count").replaceChildren(document.createTextNode(data.revision+" "),textNode("small","eventos"));$("last-sync").textContent="Sincronizado "+timeText(data.server_time);$("system-message").textContent=data.state.message;
 for(const event of data.events)history.set(event.seq,event);cursor=data.cursor;
 updateGraph("inventario",data.state.inventory,data.last_transitions.inventario);updateGraph("operacion",data.state.operation,data.last_transitions.operacion);
 if(mode==="control"){
  if(!busy){$("presence").checked=data.state.presence;$("sensor-connected").checked=data.state.hardware_connected;}
  $("locker").classList.toggle("open",!data.state.door_closed);$("locker").classList.toggle("present",data.state.presence);$("locker-led").className="led "+data.led;$("locker-led").setAttribute("aria-label","LED "+data.led.replaceAll("_"," "));$("door-status").textContent="Puerta "+(data.state.door_closed?"cerrada":"abierta");$("led-status").textContent="LED "+data.led.replaceAll("_"," ");$("locker-presence-label").textContent="Sensor: "+(data.state.presence?"objeto presente":"vacío");
  $("loan-info").textContent=data.active_loan?`Préstamo #${data.active_loan.id} · Responsable ${data.active_loan.user_code} · ${new Date(data.active_loan.borrowed_at).toLocaleString("es-CO",{timeZone:"America/Bogota"})}`:"Sin préstamo activo.";
  $("camera-status").textContent=data.camera_device.status;$("model-badge").textContent=data.camera_device.model_ready?"Modelo activo":"Modelo pendiente";$("model-badge").className="pill "+(data.camera_device.model_ready?"success":"warning");$("model-help").hidden=data.camera_device.model_ready;
  if(!data.camera_device.preview_ready){$("camera-image").hidden=true;$("camera-placeholder").hidden=false;}
  updateControls();
 }
 renderHistory();
}

function renderHistory(){
 const filter=$("history-filter").value;let events=Array.from(history.values()).sort((a,b)=>b.seq-a.seq);
 if(filter==="transitions")events=events.filter(event=>event.machine);if(filter==="rejected")events=events.filter(event=>!event.accepted||event.current==="Incidencia");
 $("history-total").textContent=history.size+" eventos recibidos";const body=$("history-body");body.replaceChildren();
 for(const event of events.slice(0,200)){
  const row=document.createElement("tr"),when=document.createElement("td"),source=document.createElement("td"),what=document.createElement("td"),result=document.createElement("td");
  when.append(textNode("strong","#"+event.seq),textNode("small",timeText(event.time)));source.append(sourceTag(event.source));what.append(textNode("strong",event.machine?`${event.previous} → ${event.current}`:event.event.replaceAll("_"," ")),textNode("small",event.message));
  result.append(textNode("span",!event.accepted?"Rechazado":event.current==="Incidencia"?"Incidencia":event.machine?"Transición":"Registrado",!event.accepted?"result-rejected":event.current==="Incidencia"?"result-incident":"result-ok"));row.append(when,source,what,result);body.append(row);
 }
 if(!events.length){const row=document.createElement("tr"),cell=textNode("td","No hay eventos para este filtro.","empty-state");cell.colSpan=4;row.append(cell);body.append(row);}
}

async function poll(){
 let delay=500;
 try{const response=await fetch("/api/estado?desde="+cursor,{cache:"no-store",signal:AbortSignal.timeout(4000)});if(!response.ok)throw new Error("Sin respuesta");const data=await response.json();if(data.revision<cursor){history.clear();cursor=0;return;}
 online=true;$("connection").textContent="Conectado";$("connection").className="connection";$("offline-banner").hidden=true;render(data);if(data.has_more)delay=10;
 }catch(error){online=false;$("connection").textContent="Desconectado";$("connection").className="connection offline";$("offline-banner").hidden=false;updateControls();delay=1500;}finally{setTimeout(poll,delay);}
}

function actionId(){return globalThis.crypto?.randomUUID?.()||Array.from(globalThis.crypto.getRandomValues(new Uint8Array(16)),v=>v.toString(16).padStart(2,"0")).join("");}
async function send(action,payload={}){
 if(!online||busy)return;busy=true;updateControls();
 const signature=JSON.stringify({action,payload});
 const envelope=pendingAction?.signature===signature?pendingAction.envelope:{action,payload,id:actionId()};pendingAction={signature,envelope};
 try{const response=await fetch("/api/acciones",{method:"POST",headers:{"Content-Type":"application/json","X-Control-Token":token},body:JSON.stringify(envelope),signal:AbortSignal.timeout(12000)});const result=await response.json();pendingAction=null;toast(result.message,!result.ok);}
 catch(error){toast("No se pudo confirmar el resultado. Consulta el historial; al repetir la misma acción se reutilizará su identificador.",true,true);}
 finally{busy=false;updateControls();}
}

if(mode==="control"){
 document.querySelectorAll("[data-action]").forEach(button=>button.addEventListener("click",()=>send(button.dataset.action,{code:$("user-code").value.trim()})));
 $("user-code").addEventListener("input",updateControls);$("presence").addEventListener("change",event=>send("presencia",{value:event.target.checked}));$("sensor-connected").addEventListener("change",event=>send("conexion_sensor",{value:event.target.checked}));
 $("start-camera").addEventListener("click",()=>send("camara_iniciar",{source:Number($("camera-source").value),roi:["x","y","w","h"].map(key=>Number($("roi-"+key).value))}));$("stop-camera").addEventListener("click",()=>send("camara_detener"));
 $("capture-image").addEventListener("click",()=>send("capturar",{label:$("capture-label").value,split:$("capture-split").value,session:$("capture-session").value.trim()}));
 $("camera-image").addEventListener("load",()=>{$("camera-image").hidden=false;$("camera-placeholder").hidden=true;});$("camera-image").addEventListener("error",()=>{$("camera-image").hidden=true;$("camera-placeholder").hidden=false;});
 setInterval(()=>{if(online&&snapshot?.camera_device.preview_ready)$("camera-image").src="/api/camara/imagen?t="+Date.now();},800);
 fetch("/api/conexion").then(response=>response.json()).then(data=>{$("tablet-urls").replaceChildren();for(const url of data.urls){const link=textNode("a",url);link.href=url;link.target="_blank";link.rel="noopener";$("tablet-urls").append(link);}if(!data.urls.length)$("tablet-urls").textContent="Consulta la dirección IPv4 del computador con ipconfig.";}).catch(()=>$("tablet-urls").textContent="Consulta la dirección IPv4 con ipconfig y abre http://IP:8000/monitor.");
}
$("history-filter").addEventListener("change",renderHistory);
if($("focus-diagrams"))$("focus-diagrams").addEventListener("click",()=>{const focused=document.body.classList.toggle("focus-mode");$("focus-diagrams").setAttribute("aria-pressed",String(focused));$("focus-diagrams").textContent=focused?"Vista completa":"Ampliar diagramas";window.scrollTo({top:0,behavior:"instant"});});
poll();
