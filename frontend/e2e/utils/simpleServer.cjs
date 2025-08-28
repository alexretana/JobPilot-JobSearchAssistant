const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 5173;

// Simple static file server
const server = http.createServer((req, res) => {
  // For now, always serve the index.html file
  const filePath = path.join(__dirname, '..', '..', 'index.html');
  
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(500);
      res.end('Error loading index.html');
      return;
    }
    
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(data);
  });
});

server.listen(PORT, () => {
  console.log(`Test server running at http://localhost:${PORT}`);
});

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('Shutting down test server...');
  server.close(() => {
    console.log('Test server closed.');
    process.exit(0);
  });
});

module.exports = { server };