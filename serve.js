const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;

http.createServer((req, res) => {
  let filePath = '.' + (req.url === '/' ? '/index.html' : req.url);
  let ext = path.extname(filePath);

  let contentType = 'text/html';
  if (ext === '.js') contentType = 'text/javascript';
  if (ext === '.json') contentType = 'application/json';
  if (ext === '.css') contentType = 'text/css';
  if (ext === '.png') contentType = 'image/png';
  if (ext === '.jpg') contentType = 'image/jpeg';

  fs.readFile(filePath, (err, content) => {
    if (err) {
      res.writeHead(404);
      res.end('File not found');
    } else {
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content);
    }
  });
}).listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
