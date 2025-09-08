# Logging Configuration

## Backend (Python/FastAPI)

The backend uses Python's standard logging module with the following configuration:

1. **Output Destinations**:
   - Console (stdout): INFO level and above
   - Log Files: All levels (DEBUG and above)

2. **File Naming Convention**:
   - Files are named with the date prefix followed by `-backend.log`
   - Example: `20230515-backend.log`

3. **Log Format**:
   ```
   [Timestamp] - [Logger Name] - [Level] - [Message]
   ```

4. **File Location**:
   - Log files are stored in the `backend/logs` directory

## Frontend (SolidJS/TypeScript)

The frontend has three types of logs:

### 1. Client Application Logs
These are logs from the SolidJS application running in the browser.

1. **Output Destinations**:
   - Browser Console: All levels (DEBUG and above)
   - In-memory buffer: All levels (for export)

2. **File Naming Convention**:
   - When exported, files use date prefix followed by `-frontend-client.log`
   - Example: `20230515-frontend-client.log`

3. **Log Format**:
   ```
   [ISO Timestamp] - [Logger Name] - [Level] - [Message]
   ```

4. **Export**: 
   - Access the debug panel in the bottom-right corner (only in development mode)
   - Click "Export Frontend Logs" to download the log file

### 2. Frontend Server Logs (Vite Development Server)
These are logs from the Vite development server itself.

1. **Output Destinations**:
   - Console (stdout): All logs
   - Log Files: All logs

2. **File Naming Convention**:
   - Files are named with the date prefix followed by `-frontend-server.log`
   - Example: `20230515-frontend-server.log`

3. **File Location**:
   - Log files are stored in the `frontend/logs` directory

4. **Log Format**:
   ```
   [ISO Timestamp] [VITE] [Level] Message
   ```

## Viewing Logs

### Backend Logs
```bash
# View INFO and above in real-time
tail -f backend/logs/*-backend.log

# View all logs for today
cat backend/logs/$(date +%Y%m%d)-backend.log
```

### Frontend Client Logs
1. Open the application in development mode
2. Click the "Debug" button in the bottom-right corner
3. Select "Export Frontend Logs"
4. The file will be downloaded with the naming convention `YYYYMMDD-frontend-client.log`

### Frontend Server Logs
```bash
# View all logs in real-time
tail -f frontend/logs/*-frontend-server.log

# View logs for today
cat frontend/logs/$(date +%Y%m%d)-frontend-server.log
```

## Log Directory Structure

```
project/
├── backend/
│   └── logs/
│       └── YYYYMMDD-backend.log
├── frontend/
│   └── logs/
│       └── YYYYMMDD-frontend-server.log
└── (exported client logs go to browser downloads)
```

## Configuration

### Backend
The logging level can be adjusted by modifying the `level` parameter in `logging.basicConfig()` in `backend/api/main.py`.

### Frontend Client
The logging level can be adjusted by changing the `CURRENT_LOG_LEVEL` constant in `frontend/src/utils/logger.ts`.

### Frontend Server
The Vite server logging is configured in `frontend/vite.config.ts`.