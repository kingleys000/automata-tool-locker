// Servidor aislado del módulo de simulación. No utiliza el portal de cámara.
const assert = require('node:assert/strict');
const {spawn} = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require(process.argv[2] || 'playwright');

(async () => {
  fs.mkdirSync('artifacts', {recursive:true});
  const server=spawn(path.resolve('.venv/Scripts/python.exe'),['-u','run_simulador.py','--port','8102','--host','127.0.0.1'],{windowsHide:true,stdio:['ignore','pipe','pipe']});
  let browser;
  try {
    await new Promise((resolve,reject)=>{
      const timeout=setTimeout(()=>reject(new Error('No inició el simulador')),15000);
      server.once('error',error=>{clearTimeout(timeout);reject(error);});
      server.stdout.on('data',data=>{if(data.toString().includes('Simulador:')){clearTimeout(timeout);resolve();}});
      server.stderr.on('data',data=>process.stderr.write(data));
    });
    browser=await chromium.launch({headless:true,channel:'msedge'});
    const errors=[];
    const control=await browser.newPage({viewport:{width:1440,height:1000}});
    const tablet=await browser.newPage({viewport:{width:1280,height:800}});
    for(const page of [control,tablet]){
      page.on('pageerror',error=>errors.push(error.message));
      page.on('console',message=>{if(message.type()==='error' && /Content Security Policy|Refused to/.test(message.text()))errors.push(message.text());});
    }
    await control.goto('http://127.0.0.1:8102/simulador');
    await tablet.goto('http://127.0.0.1:8102/automatas');
    await control.locator('#connection').filter({hasText:'Sincronizado'}).waitFor();
    await tablet.locator('#connection').filter({hasText:'Sincronizado'}).waitFor();
    assert.equal(await tablet.locator('#scene,#manual-controls,#play').count(),0);
    assert.equal(await tablet.locator('.automaton').count(),2);
    assert.equal(await tablet.locator('.graph-node.active').count(),2);
    assert.equal(await tablet.evaluate(()=>document.documentElement.scrollHeight<=innerHeight+2),true,'Tablet horizontal sin recortes');
    await control.screenshot({path:'artifacts/simulador-desktop.png',fullPage:true});
    await tablet.screenshot({path:'artifacts/simulador-tablet.png',fullPage:true});

    const next=async()=>{
      const before=(await (await control.request.get('http://127.0.0.1:8102/api/simulacion/estado')).json()).revision;
      await control.locator('#step').click();
      await control.waitForFunction(before=>Number(document.getElementById('event-number').textContent.replace(/\D/g,''))>before,before);
    };
    await next();
    await tablet.locator('#inventory-state').filter({hasText:'Reservada'}).waitFor();
    await next();
    assert.match(await control.locator('#door').getAttribute('class'),/open/);
    await control.screenshot({path:'artifacts/simulador-puerta-abierta.png',fullPage:true,animations:'disabled'});
    for(let i=0;i<13;i++)await next();
    await tablet.locator('#inventory-state').filter({hasText:'Disponible'}).waitFor();
    let state=(await (await control.request.get('http://127.0.0.1:8102/api/simulacion/estado')).json()).state;
    assert.equal(state.loan_count,1);assert.equal(state.returned_count,1);assert.equal(state.loan_active,false);

    await control.selectOption('#scenario','fallo');
    await control.locator('#play').click();
    await control.locator('#demo-progress').filter({hasText:'Paso'}).waitFor();
    await control.locator('#pause').click();
    await control.locator('#demo-progress').filter({hasText:'Pausa'}).waitFor();
    const paused=(await (await control.request.get('http://127.0.0.1:8102/api/simulacion/estado')).json()).demo.index;
    await next();
    assert.equal((await (await control.request.get('http://127.0.0.1:8102/api/simulacion/estado')).json()).demo.index,paused+1);
    await control.selectOption('#speed','0.8');
    await control.locator('#pause').filter({hasText:'Continuar'}).click();
    await tablet.locator('#operation-state').filter({hasText:'Incidencia'}).waitFor({timeout:30000});
    await tablet.screenshot({path:'artifacts/simulador-incidencia.png',fullPage:true});
    await control.locator('#demo-progress').filter({hasText:'Completado'}).waitFor({timeout:30000});
    await tablet.locator('#inventory-state').filter({hasText:'Disponible'}).waitFor();
    await tablet.context().setOffline(true);
    await tablet.locator('#offline').waitFor({state:'visible'});
    await tablet.context().setOffline(false);
    await tablet.locator('#offline').waitFor({state:'hidden'});
    await control.locator('#view-right').click();
    assert.match(await control.locator('#world').getAttribute('style'),/rotateY\(-16deg\)/);

    for(const [page,name,size] of [[tablet,'simulador-tablet-vertical',{width:800,height:1280}],[control,'simulador-mobile',{width:390,height:844}]]){
      await page.setViewportSize(size);
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,name+' sin desborde horizontal');
      await page.screenshot({path:'artifacts/'+name+'.png',fullPage:true});
    }
    assert.deepEqual(errors,[]);
    console.log('Simulador verificado: ciclo manual, reproducción, pausa, paso, fallo, recuperación, sincronización, reconexión, escena 3D y diseños adaptables.');
  } finally {
    if(browser)await browser.close();
    server.kill();
  }
})().catch(error=>{console.error(error);process.exitCode=1;});
