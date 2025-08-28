import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';

// Convert import.meta.url to __dirname equivalent
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

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

export { server };