#!/bin/bash

# Check if --subprocess flag is provided
SUBPROCESS_MODE=0
if [[ "$1" == "--subprocess" ]]; then
    SUBPROCESS_MODE=1
fi

echo "Starting JobPilot servers..."

# Function to clean up background processes on exit
cleanup() {
    echo -e "\nShutting down servers..."
    
    # Kill frontend server if running
    if [[ -n $FRONTEND_PID ]]; then
        echo "Killing frontend server..."
        kill $FRONTEND_PID 2>/dev/null
        wait $FRONTEND_PID 2>/dev/null
    fi
    
    # Kill backend server if in subprocess mode
    if [[ $SUBPROCESS_MODE -eq 1 && -n $BACKEND_PID ]]; then
        echo "Killing backend server..."
        kill $BACKEND_PID 2>/dev/null
        wait $BACKEND_PID 2>/dev/null
    fi
    
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start backend server
if [[ $SUBPROCESS_MODE -eq 1 ]]; then
    echo "Starting backend server in subprocess mode..."
    (cd backend && python -m api.main) &
    BACKEND_PID=$!
    echo "Backend server started with PID: $BACKEND_PID"
else
    echo "Starting backend server in subprocess mode..."
    (cd backend && python -m api.main) &
    BACKEND_PID=$!
    echo "Backend server started with PID: $BACKEND_PID"
fi

# Start frontend server as subprocess
echo "Starting frontend server in subprocess mode..."
(cd frontend && npm run dev) &
FRONTEND_PID=$!
echo "Frontend server started with PID: $FRONTEND_PID"

# Wait for user input if not in subprocess mode
if [[ $SUBPROCESS_MODE -eq 0 ]]; then
    echo "Press Ctrl+C to stop servers..."
    wait $FRONTEND_PID
fi

# If we get here, frontend server was stopped
echo "Frontend server stopped."

# Kill backend server if in subprocess mode
if [[ $SUBPROCESS_MODE -eq 1 ]]; then
    echo "Killing backend server..."
    kill $BACKEND_PID 2>/dev/null
    wait $BACKEND_PID 2>/dev/null
fi

echo "All servers stopped."