// Simple logger utility that mirrors backend logging format
const LOG_LEVELS = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3
};

// Current log level (can be adjusted for more or less verbosity)
const CURRENT_LOG_LEVEL = LOG_LEVELS.DEBUG;

// Format timestamp similar to backend
const formatTimestamp = () => {
  const now = new Date();
  return now.toISOString();
};

// Format log message similar to backend
const formatLogMessage = (level: string, name: string, message: string) => {
  return `${formatTimestamp()} - ${name} - ${level} - ${message}`;
};

// Log to console with appropriate styling
const logToConsole = (level: string, name: string, message: string, ...args: any[]) => {
  const formattedMessage = formatLogMessage(level, name, message);
  
  switch (level) {
    case 'DEBUG':
      if (CURRENT_LOG_LEVEL <= LOG_LEVELS.DEBUG) {
        console.debug(formattedMessage, ...args);
      }
      break;
    case 'INFO':
      if (CURRENT_LOG_LEVEL <= LOG_LEVELS.INFO) {
        console.info(formattedMessage, ...args);
      }
      break;
    case 'WARN':
      if (CURRENT_LOG_LEVEL <= LOG_LEVELS.WARN) {
        console.warn(formattedMessage, ...args);
      }
      break;
    case 'ERROR':
      if (CURRENT_LOG_LEVEL <= LOG_LEVELS.ERROR) {
        console.error(formattedMessage, ...args);
      }
      break;
  }
};

// Simple in-memory log storage for export
let logBuffer: string[] = [];

// Add log entry to buffer (for export)
const addToBuffer = (level: string, name: string, message: string) => {
  // Only keep last 10000 log entries to prevent memory issues
  if (logBuffer.length > 10000) {
    logBuffer.shift();
  }
  logBuffer.push(formatLogMessage(level, name, message));
};

// Logger class
class Logger {
  private name: string;

  constructor(name: string) {
    this.name = name;
  }

  debug(message: string, ...args: any[]) {
    logToConsole('DEBUG', this.name, message, ...args);
    addToBuffer('DEBUG', this.name, message);
  }

  info(message: string, ...args: any[]) {
    logToConsole('INFO', this.name, message, ...args);
    addToBuffer('INFO', this.name, message);
  }

  warn(message: string, ...args: any[]) {
    logToConsole('WARN', this.name, message, ...args);
    addToBuffer('WARN', this.name, message);
  }

  error(message: string, ...args: any[]) {
    logToConsole('ERROR', this.name, message, ...args);
    addToBuffer('ERROR', this.name, message);
  }
}

// Export logs as a file
export const exportFrontendLogs = () => {
  try {
    // Get current date for filename
    const date = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    const filename = `${date}-frontend-client.log`;
    
    // Format all logs
    const logContent = logBuffer.join('\n');
    
    // Create Blob and download
    const blob = new Blob([logContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    
    // Create temporary link and trigger download
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    
    // Cleanup
    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 0);
    
    console.info(`Frontend logs exported to ${filename}`);
  } catch (error) {
    console.error('Failed to export frontend logs:', error);
  }
};

// Get log buffer for programmatic access
export const getLogBuffer = () => {
  return [...logBuffer];
};

// Clear log buffer
export const clearLogBuffer = () => {
  logBuffer = [];
};

// Factory function to create a logger
export const createLogger = (name: string) => {
  return new Logger(name);
};

// Default export
export default Logger;