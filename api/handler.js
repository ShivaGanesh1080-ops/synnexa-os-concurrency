/**
 * Vercel Serverless Function API Entry Handler for SYNNEXA
 * Dispatches incoming serverless requests to src/routes/api.js
 */

const path = require('path');
const fs = require('fs');
const { handleApiRequest } = require('../src/routes/api');

async function parseRequestBody(req) {
  if (req.body) {
    if (typeof req.body === 'object') return req.body;
    if (typeof req.body === 'string') {
      try {
        return JSON.parse(req.body);
      } catch (e) {
        return {};
      }
    }
  }

  return new Promise((resolve) => {
    let bodyData = '';
    req.on('data', chunk => {
      bodyData += chunk;
      if (bodyData.length > 5e6) {
        req.destroy();
        resolve({});
      }
    });
    req.on('end', () => {
      if (!bodyData) return resolve({});
      try {
        resolve(JSON.parse(bodyData));
      } catch (e) {
        resolve({});
      }
    });
    req.on('error', () => resolve({}));
  });
}

module.exports = async (req, res) => {
  // CORS & Security Headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  const host = req.headers['x-forwarded-host'] || req.headers.host || 'localhost';
  const proto = req.headers['x-forwarded-proto'] || 'https';
  const parsedUrl = new URL(req.url, `${proto}://${host}`);
  let pathname = parsedUrl.pathname;
  if (pathname.length > 1 && pathname.endsWith('/')) {
    pathname = pathname.slice(0, -1);
  }

  // Handle Presentation Deck Download
  if (pathname === '/download-ppt' || pathname === '/download-presentation' || pathname === '/presentation.pptx' || pathname === '/deck.pptx' || pathname === '/ppt') {
    const rootPpt = path.join(__dirname, '..', 'SyncReg_OS_Product8_Presentation.pptx');
    const publicPpt = path.join(__dirname, '..', 'public', 'SyncReg_OS_Product8_Presentation.pptx');
    const fileToServe = fs.existsSync(publicPpt) ? publicPpt : (fs.existsSync(rootPpt) ? rootPpt : null);

    if (fileToServe) {
      res.writeHead(200, {
        'Content-Type': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'Content-Disposition': 'attachment; filename="SyncReg_OS_Product8_Presentation.pptx"'
      });
      fs.createReadStream(fileToServe).pipe(res);
      return;
    }
  }

  const body = await parseRequestBody(req);
  await handleApiRequest(req, res, pathname, parsedUrl.searchParams, body);
};
