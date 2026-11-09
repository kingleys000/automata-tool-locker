// Utilidades compartidas de las pruebas de navegador: intérprete Python del
// proyecto y lanzamiento portable del navegador.
const path = require('node:path');
const os = require('node:os');
const fs = require('node:fs');

const root = path.join(__dirname, '..');
const localBrowsersPath = path.join(root, '.tools', 'ms-playwright');
if (!process.env.PLAYWRIGHT_BROWSERS_PATH && fs.existsSync(localBrowsersPath)) {
  process.env.PLAYWRIGHT_BROWSERS_PATH = localBrowsersPath;
}

function pythonBin() {
  if (process.env.PYTHON_BIN) return process.env.PYTHON_BIN;
  const local = os.platform() === 'win32' ? '.venv/Scripts/python.exe' : '.venv/bin/python';
  return path.join(root, local);
}

function browserLaunchOptions() {
  const options = {headless: true};
  if (process.env.BROWSER_CHANNEL) options.channel = process.env.BROWSER_CHANNEL;
  else if (os.platform() === 'win32') options.channel = 'msedge';
  return options;
}

module.exports = {pythonBin, browserLaunchOptions, root};
