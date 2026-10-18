// Smoke test del portal real, sin activar cámara ni escribir en la base de datos.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require(process.argv[2] || 'playwright');
const baseUrl = process.argv[3] || 'http://127.0.0.1:8000';
(async () => {
  const browser = await chromium.launch({headless: true, channel: 'msedge'});
  const errors = [];
  fs.mkdirSync('artifacts', {recursive:true});
  for (const [name, route, viewport] of [
    ['control-desktop','control',{width:1440,height:1000}],
    ['monitor-tablet','monitor',{width:1280,height:800}],
    ['monitor-portrait','monitor',{width:800,height:1280}],
    ['control-mobile','control',{width:390,height:844}],
  ]) {
    const page = await browser.newPage({viewport});
    page.on('pageerror',error=>errors.push(error.message));
    await page.goto(baseUrl+'/'+route);
    await page.locator('#connection').filter({hasText:'Conectado'}).waitFor();
    assert.equal(await page.locator('.automaton-svg').count(),2);
    assert.equal(await page.locator('.graph-node.active').count(),2);
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true, name+' horizontal overflow');
    if(route==='monitor')assert.equal(await page.locator('[data-action]').count(),0);
    await page.screenshot({path:path.join('artifacts',name+'.png'),fullPage:true});
    if(name==='monitor-tablet'){
      await page.getByRole('button',{name:'Ampliar diagramas'}).click();
      const bounds=await page.locator('.graphs').boundingBox();
      assert.ok(bounds.y+bounds.height<viewport.height,'Diagramas completos dentro de la tablet horizontal');
      await page.screenshot({path:path.join('artifacts','monitor-exposicion.png'),fullPage:true});
      await page.context().setOffline(true);
      await page.locator('#offline-banner').waitFor({state:'visible'});
      await page.context().setOffline(false);
      await page.locator('#connection').filter({hasText:'Conectado'}).waitFor();
      await page.locator('#offline-banner').waitFor({state:'hidden'});
    }
    await page.close();
  }
  await browser.close();
  assert.deepEqual(errors,[]);
  console.log('Portal verificado en escritorio, tablet horizontal/vertical y móvil; reconexión correcta.');
})().catch(error=>{console.error(error);process.exit(1)});
