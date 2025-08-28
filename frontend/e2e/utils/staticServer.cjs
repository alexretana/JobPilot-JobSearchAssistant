const express = require('express');
const path = require('path');

const app = express();
const port = 5173;

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, '..', '..', 'public')));

// Serve index.html for all routes (client-side routing)
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '..', '..', 'index.html'));
});

const server = app.listen(port, () => {
  console.log(`Test server running at http://localhost:${port}`);
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