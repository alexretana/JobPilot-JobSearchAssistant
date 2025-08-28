# Frontend Development Guide

This document provides information about the frontend design and how to run the JobPilot application.

## Frontend Technology Stack

The frontend is built using:
- SolidJS for the UI framework
- Vite for the build tool
- TailwindCSS for styling
- TypeScript for type safety

## Project Structure

```
frontend/
├── src/              # Source code
├── public/           # Static assets
├── dist/             # Built files
├── package.json      # Dependencies and scripts
├── vite.config.ts    # Vite configuration
└── tailwind.config.js # Tailwind configuration
```

## Running the Application

### Normal Mode

To run both the frontend and backend servers in normal mode:

```bash
# On Windows
run_all.bat

# On Linux/Mac
./run_all.sh
```

In this mode:
- Both frontend and backend run as subprocesses
- The terminal will show output from both servers
- Press Ctrl+C to stop both servers

### Subprocess Mode

To run both servers as background processes:

```bash
# On Windows
run_all.bat --subprocess

# On Linux/Mac
./run_all.sh --subprocess
```

In this mode:
- Both frontend and backend run in the background
- The terminal is returned to you immediately
- Servers continue running until manually stopped

## Development Workflow

1. Make changes to the frontend code in the `src/` directory
2. The Vite development server will automatically reload the browser
3. For backend changes, you may need to restart the servers

## Building for Production

To build the frontend for production:

```bash
cd frontend
npm run build
```

The built files will be in the `dist/` directory.