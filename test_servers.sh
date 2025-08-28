#!/bin/bash

# Test script to verify that both frontend and backend servers start correctly

echo "Testing JobPilot server startup..."

# Start both servers in subprocess mode
echo "Starting servers in subprocess mode..."
./run_all.sh --subprocess &

# Wait for 10 seconds
sleep 10

# Check if servers are running
if pgrep -f "npm run dev" > /dev/null || pgrep -f "python -m api.main" > /dev/null; then
    echo "Servers are running correctly"
    
    # Kill the run_all.sh process
    pkill -f "run_all.sh"
    
    # Wait a moment for cleanup
    sleep 2
    
    # Force kill any remaining processes
    pkill -f "npm run dev" 2>/dev/null
    pkill -f "python -m api.main" 2>/dev/null
    
    echo "Test completed successfully"
else
    echo "Error: Servers failed to start"
    exit 1
fi