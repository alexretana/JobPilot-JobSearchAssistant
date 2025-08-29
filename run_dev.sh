#!/bin/bash

echo "Starting JobPilot development servers..."

# Function to clean up background processes on exit
cleanup() {
    echo -e "\nShutting down servers..."
    
    # Kill frontend server if running
    if [[ -n $FRONTEND_PID ]]; then
        echo "Killing frontend server..."
        kill $FRONTEND_PID 2>/dev/null
        wait $FRONTEND_PID 2>/dev/null
    fi
    
    # Kill backend server if running
    if [[ -n $BACKEND_PID ]]; then
        echo "Killing backend server..."
        kill $BACKEND_PID 2>/dev/null
        wait $BACKEND_PID 2>/dev/null
    fi
    
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start backend server
echo "Starting backend server..."
(cd backend && python -m api.main) &
BACKEND_PID=$!
echo "Backend server started with PID: $BACKEND_PID"

# Start frontend server
echo "Starting frontend server..."
(cd frontend && npm run dev) &
FRONTEND_PID=$!
echo "Frontend server started with PID: $FRONTEND_PID"

echo
echo "Servers started:"
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:3000"
echo
echo "Press Ctrl+C to stop servers..."

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID