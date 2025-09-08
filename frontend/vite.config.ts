import { defineConfig } from 'vite';
import solid from 'vite-plugin-solid';
import fs from 'fs';
import path from 'path';

// Create logs directory if it doesn't exist
const logsDir = path.join(__dirname, '..', 'frontend', 'logs');
if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir, { recursive: true });
}

// Create a log file with today's date
const date = new Date().toISOString().slice(0, 10).replace(/-/g, '');
const logFile = path.join(logsDir, `${date}-frontend-server.log`);

// Create a write stream for logging
const logStream = fs.createWriteStream(logFile, { flags: 'a' });

// Override console methods to also write to file
const originalLog = console.log;
const originalError = console.error;
const originalWarn = console.warn;

console.log = (...args) => {
  originalLog(...args);
  logStream.write(`[${new Date().toISOString()}] [VITE] [INFO] ${args.join(' ')}
`);
};

console.error = (...args) => {
  originalError(...args);
  logStream.write(`[${new Date().toISOString()}] [VITE] [ERROR] ${args.join(' ')}
`);
};

console.warn = (...args) => {
  originalWarn(...args);
  logStream.write(`[${new Date().toISOString()}] [VITE] [WARN] ${args.join(' ')}
`);
};

export default defineConfig({
  plugins: [solid()],
  server: {
    port: 3000,
    proxy: {
      // Proxy all API requests to the backend
      '/jobs': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/users': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/auth': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/companies': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/applications': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/resumes': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/skill-banks': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/timeline': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/job-sources': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/search': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/leads': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
  // Custom logger for Vite
  customLogger: {
    info: (msg, options) => {
      originalLog(msg);
      logStream.write(`[${new Date().toISOString()}] [VITE] [INFO] ${msg}
`);
    },
    warn: (msg, options) => {
      originalWarn(msg);
      logStream.write(`[${new Date().toISOString()}] [VITE] [WARN] ${msg}
`);
    },
    error: (msg, options) => {
      originalError(msg);
      logStream.write(`[${new Date().toISOString()}] [VITE] [ERROR] ${msg}
`);
    },
    clearScreen: () => {
      // Do nothing to prevent clearing the screen
    }
  }
});
