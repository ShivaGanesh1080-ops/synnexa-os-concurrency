/**
 * SyncReg — High-Throughput Tatkal Concurrency & Event Management Platform
 * Server Entry Point (Clean Multi-Page URL Routing & Zero-Dependency Native Node.js)
 * SR University • CSE Core • Operating Systems Lab • Product #8
 */

const http = require('http');
const url = require('url');
const fs = require('fs');
const path = require('path');
const { handleApiRequest } = require('./src/routes/api');

const PORT = process.env.PORT || 3000;
const PUBLIC_DIR = path.join(__dirname, 'public');

const MIME_TYPES = {
  '.html': 'text/html; charset=UTF-8',
  '.css': 'text/css; charset=UTF-8',
  '.js': 'application/javascript; charset=UTF-8',
  '.json': 'application/json; charset=UTF-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
  '.pdf': 'application/pdf'
};

const server = http.createServer((req, res) => {
  // CORS & Security Headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const pathname = parsedUrl.pathname;
  let cleanPath = pathname;
  if (cleanPath.length > 1 && cleanPath.endsWith('/')) {
    cleanPath = cleanPath.slice(0, -1);
  }

  // 1. API Handlers
  if (pathname.startsWith('/api/')) {
    let bodyData = '';
    req.on('data', chunk => {
      bodyData += chunk;
      if (bodyData.length > 5e6) {
        res.writeHead(413, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'PAYLOAD_TOO_LARGE' }));
        req.destroy();
      }
    });

    req.on('end', async () => {
      let parsedBody = {};
      if (bodyData) {
        try {
          parsedBody = JSON.parse(bodyData);
        } catch (e) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'INVALID_JSON', message: 'Malformed JSON payload.' }));
          return;
        }
      }

      await handleApiRequest(req, res, pathname, parsedUrl.searchParams, parsedBody);
    });

    return;
  }

  // 2. PowerPoint Deck Download Endpoint
  if (cleanPath === '/download-ppt' || cleanPath === '/download-presentation' || cleanPath === '/presentation.pptx' || cleanPath === '/SyncReg_OS_Product8_Presentation.pptx' || cleanPath === '/deck.pptx' || cleanPath === '/ppt') {
    const pptFile = path.join(__dirname, 'SyncReg_OS_Product8_Presentation.pptx');
    const publicPpt = path.join(PUBLIC_DIR, 'SyncReg_OS_Product8_Presentation.pptx');
    const fileToServe = fs.existsSync(pptFile) ? pptFile : (fs.existsSync(publicPpt) ? publicPpt : null);

    if (fileToServe) {
      res.writeHead(200, {
        'Content-Type': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'Content-Disposition': 'attachment; filename="SyncReg_OS_Product8_Presentation.pptx"'
      });
      fs.createReadStream(fileToServe).pipe(res);
      return;
    }
  }

  // 3. Multi-Page Clean URL Routing
  let targetFile = null;
  if (cleanPath === '/' || cleanPath === '/index' || cleanPath === '/user' || cleanPath === '/portal' || cleanPath === '/events') {
    targetFile = 'index.html';
  } else if (cleanPath === '/studio' || cleanPath === '/concurrency' || cleanPath === '/benchmark') {
    targetFile = 'studio.html';
  } else if (cleanPath === '/admin' || cleanPath === '/organizer' || cleanPath === '/hackathon-admin' || cleanPath === '/platform' || cleanPath === '/settings' || cleanPath === '/platform-admin') {
    targetFile = 'admin.html';
  }

  if (targetFile) {
    const pagePath = path.join(PUBLIC_DIR, targetFile);
    if (fs.existsSync(pagePath)) {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=UTF-8' });
      fs.createReadStream(pagePath).pipe(res);
      return;
    }
  }

  // 4. Static Asset Serving (CSS, JS, Images)
  let safePath = pathname.replace(/^\/+/, '');
  let filePath = path.join(PUBLIC_DIR, safePath);

  if (!filePath.startsWith(PUBLIC_DIR)) {
    res.writeHead(403, { 'Content-Type': 'text/plain' });
    res.end('403 Forbidden');
    return;
  }

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      // Fallback
      const indexPath = path.join(PUBLIC_DIR, 'index.html');
      if (fs.existsSync(indexPath)) {
        res.writeHead(200, { 'Content-Type': 'text/html; charset=UTF-8' });
        fs.createReadStream(indexPath).pipe(res);
        return;
      }

      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('404 Not Found');
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    res.writeHead(200, { 'Content-Type': contentType });
    fs.createReadStream(filePath).pipe(res);
  });
});

server.listen(PORT, () => {
  console.log(`================================================================`);
  console.log(`  SyncReg — Production Concurrency Platform (Node.js)`);
  console.log(`  Operating Systems Lab • Product #8 • SR University`);
  console.log(`  • Hub / Landing & Team:  http://localhost:${PORT}/`);
  console.log(`  • Participant Portal:    http://localhost:${PORT}/user`);
  console.log(`  • Tatkal Concurrency:    http://localhost:${PORT}/studio`);
  console.log(`  • Hackathon Admin:       http://localhost:${PORT}/admin`);
  console.log(`  • Platform Admin:        http://localhost:${PORT}/platform`);
  console.log(`================================================================`);
});
