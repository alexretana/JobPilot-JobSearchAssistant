#!/usr/bin/env python3
"""
Script to run both frontend and backend servers as subprocesses.
This script manages both processes and ensures proper cleanup.
"""

import subprocess
import sys
import time
import requests
import signal
import os
from typing import List

# Global variables to track processes
processes: List[subprocess.Popen] = []
frontend_port = 3000
backend_port = 8000


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\nShutting down servers...")
    for proc in processes:
        if proc.poll() is None:  # Process is still running
            proc.terminate()
    
    # Wait for processes to terminate
    for proc in processes:
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    
    print("All servers stopped.")
    sys.exit(0)


def start_backend() -> subprocess.Popen:
    """Start the backend server"""
    print("Starting backend server...")
    # Run the API directly with Python
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "api.main"],
        cwd=os.path.join(os.getcwd(), "backend"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    processes.append(backend_process)
    return backend_process


def start_frontend() -> subprocess.Popen:
    """Start the frontend server"""
    print("Starting frontend server...")
    # Run npm dev in the frontend directory
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=os.path.join(os.getcwd(), "frontend"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    processes.append(frontend_process)
    return frontend_process


def check_port(port: int, service_name: str) -> bool:
    """Check if a service is running on the specified port"""
    try:
        response = requests.get(f"http://localhost:{port}", timeout=1)
        return response.status_code < 500  # Any response is good
    except requests.exceptions.RequestException:
        return False


def wait_for_services(timeout: int = 30) -> bool:
    """Wait for both services to be responsive"""
    start_time = time.time()
    
    backend_ready = False
    frontend_ready = False
    
    while time.time() - start_time < timeout:
        if not backend_ready and check_port(backend_port, "backend"):
            backend_ready = True
            print(f"✓ Backend server is running on port {backend_port}")
        
        if not frontend_ready and check_port(frontend_port, "frontend"):
            frontend_ready = True
            print(f"✓ Frontend server is running on port {frontend_port}")
        
        if backend_ready and frontend_ready:
            return True
            
        time.sleep(1)
    
    # Check what failed to start
    if not backend_ready:
        print(f"✗ Backend server failed to start on port {backend_port}")
    if not frontend_ready:
        print(f"✗ Frontend server failed to start on port {frontend_port}")
    
    return False


def main():
    """Main function to run both servers"""
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("Starting JobPilot development servers...")
    
    try:
        # Start both servers
        backend_process = start_backend()
        frontend_process = start_frontend()
        
        # Give processes a moment to start
        time.sleep(2)
        
        # Check if processes started successfully
        if backend_process.poll() is not None:
            print("✗ Backend process failed to start")
            print("Backend stderr:", backend_process.stderr.read() if backend_process.stderr else "No error output")
            return 1
            
        if frontend_process.poll() is not None:
            print("✗ Frontend process failed to start")
            print("Frontend stderr:", frontend_process.stderr.read() if frontend_process.stderr else "No error output")
            return 1
        
        print("Waiting for servers to be ready...")
        
        # Wait for services to be ready
        if wait_for_services():
            print("\n🎉 Both servers are running!")
            print(f"   Frontend: http://localhost:{frontend_port}")
            print(f"   Backend:  http://localhost:{backend_port}")
            print("\nPress Ctrl+C to stop servers...")
            
            # Keep the script running
            try:
                while True:
                    # Check if any process has died
                    for i, proc in enumerate(processes):
                        if proc.poll() is not None:
                            service_name = "backend" if i == 0 else "frontend"
                            print(f"\n{service_name.capitalize()} process has stopped unexpectedly")
                            return 1
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
        else:
            print("Failed to start one or both servers")
            return 1
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Make sure you have the required dependencies installed:")
        print("  - Python with required packages (see backend/requirements.txt)")
        print("  - Node.js and npm with frontend dependencies (run 'npm install' in frontend directory)")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())