// Un ciclo completo desde los botones reales y un segundo navegador de lectura.
// Usa observaciones controladas SOLO en tests/browser_fixture.py.
const assert = require('node:assert/strict');
const {spawn} = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require(process.argv[2] || 'playwright');
(async()=>{
  const server = spawn(path.resolve('.venv/Scripts/python.exe'),['-u','tests/browser_fixture.py'],{windowsHide:true,stdio:['pipe','pipe','pipe']});
  let browser;
  try{
    await new Promise((resolve,reject)=>{const timer=setTimeout(()=>reject(new Error('Fixture no inicia')),15000);server.once('error',reject);server.stdout.on('data',chunk=>{if(chunk.toString().includes('UI_FIXTURE_READY')){clearTimeout(timer);resolve();}});server.stderr.on('data',chunk=>process.stderr.write(chunk));});
    browser=await chromium.launch({headless:true,channel:'msedge'});
    const control=await browser.newPage({viewport:{width:1440,height:1000}});
    const monitor=await browser.newPage({viewport:{width:1280,height:800}});
    const errors=[];control.on('pageerror',e=>errors.push(e.message));monitor.on('pageerror',e=>errors.push(e.message));
    await control.goto('http://127.0.0.1:8101/control');await monitor.goto('http://127.0.0.1:8101/monitor');
    const wait=async(page,id,value)=>page.waitForFunction(({id,value})=>document.getElementById(id)?.textContent===value,{id,value});
    const click=action=>control.locator(`[data-action="${action}"]`).click();
    await wait(control,'connection','Conectado');await wait(monitor,'connection','Conectado');
    await control.locator('#presence').check();await wait(control,'recognition-state','Martillo');
    const start=Date.now();await click('solicitar');await wait(monitor,'inventory-state','Reservada');const syncMs=Date.now()-start;
    assert.ok(syncMs<1000,`Actualización tablet: ${syncMs} ms`);
    await click('puerta_abierta');await wait(control,'operation-state','Esperando retiro');
    await control.locator('#presence').uncheck();await wait(control,'recognition-state','Vacío');
    await click('cerrar');await click('puerta_cerrada');await wait(monitor,'inventory-state','Prestada');await click('finalizar');
    await wait(control,'operation-state','Inactiva');await click('devolver');await click('puerta_abierta');
    await wait(control,'operation-state','Esperando depósito');await control.locator('#presence').check();await wait(control,'recognition-state','Martillo');
    await click('cerrar');await click('puerta_cerrada');await wait(monitor,'inventory-state','En revisión');await click('finalizar');
    await wait(control,'operation-state','Inactiva');await control.locator('#user-code').fill('ADMIN');await control.getByText('Revisión del encargado',{exact:true}).click();await click('aprobar');await wait(monitor,'inventory-state','Disponible');
    const data=await (await monitor.request.get('http://127.0.0.1:8101/api/estado')).json();
    assert.equal(data.loan_count,1);assert.equal(data.active_loan,null);assert.ok(data.loans[0].returned_at);
    assert.equal(await monitor.locator('#graph-inventario [data-state="Disponible"]').getAttribute('class'),'graph-node active');
    assert.ok(await monitor.locator('#graph-inventario .graph-edge.latest').count());assert.deepEqual(errors,[]);
    fs.writeFileSync('artifacts/browser-cycle.json',JSON.stringify({result:'passed',source:'observaciones controladas solo en tests',tablet_update_ms:syncMs,loans:data.loan_count,events:data.revision},null,2));
    console.log(`Ciclo completo de UI correcto; monitor actualizado en ${syncMs} ms. Observaciones controladas de prueba.`);
  }finally{
    if(browser)await browser.close();server.kill();
  }
})().catch(error=>{console.error(error);process.exitCode=1});
