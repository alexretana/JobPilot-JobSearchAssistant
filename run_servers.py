#!/usr/bin/env python3
"""
Script to run both frontend and backend servers and verify they're running.
"""

import subprocess
import time
import requests
import sys
import os

def check_server(port, service_name):
    """Check if a service is running on the specified port"""
    try:
        if port == 8000:
            # For backend, check the health endpoint
            response = requests.get(f"http://localhost:{port}/health", timeout=5)
        else:
            # For frontend, just check if it responds
            response = requests.get(f"http://localhost:{port}", timeout=5)
        return response.status_code < 500
    except requests.exceptions.RequestException:
        return False

def main():
    """Main function to start servers and verify they're running"""
    print("Starting JobPilot development servers...")
    
    # Start backend server
    print("Starting backend server...")
    backend_process = subprocess.Popen(
        ["python", "-m", "api.main"],
        cwd=os.path.join(os.getcwd(), "backend"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Start frontend server
    print("Starting frontend server...")
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=os.path.join(os.getcwd(), "frontend"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print("Waiting for servers to start (this may take 10-20 seconds)...")
    
    # Wait and check periodically
    backend_ready = False
    frontend_ready = False
    max_wait_time = 30  # seconds
    check_interval = 2  # seconds
    elapsed_time = 0
    
    while elapsed_time < max_wait_time:
        if not backend_ready:
            backend_ready = check_server(8000, "backend")
            if backend_ready:
                print("✓ Backend server is running on http://localhost:8000")
        
        if not frontend_ready:
            frontend_ready = check_server(3000, "frontend")
            if frontend_ready:
                print("✓ Frontend server is running on http://localhost:3000")
        
        if backend_ready and frontend_ready:
            print("\n🎉 Both servers are successfully running!")
            print("   Frontend: http://localhost:3000")
            print("   Backend:  http://localhost:8000")
            print("\nPress Ctrl+C to stop both servers...")
            
            try:
                # Keep the script running
                while True:
                    # Check if processes are still alive
                    if backend_process.poll() is not None:
                        print("Backend process has stopped")
                        break
                    if frontend_process.poll() is not None:
                        print("Frontend process has stopped")
                        break
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
            
            # Clean shutdown
            print("\nShutting down servers...")
            backend_process.terminate()
            frontend_process.terminate()
            
            try:
                backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                backend_process.kill()
                
            try:
                frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                frontend_process.kill()
                
            print("All servers stopped.")
            return 0
        
        time.sleep(check_interval)
        elapsed_time += check_interval
    
    # If we get here, one or both servers failed to start
    print("\n❌ Timeout waiting for servers to start")
    
    if not backend_ready:
        print("Backend server failed to start")
        # Try to get error output
        if backend_process.poll() is not None:
            stderr = backend_process.stderr.read().decode() if backend_process.stderr else ""
            if stderr:
                print(f"Backend error: {stderr}")
    
    if not frontend_ready:
        print("Frontend server failed to start")
        # Try to get error output
        if frontend_process.poll() is not None:
            stderr = frontend_process.stderr.read().decode() if frontend_process.stderr else ""
            if stderr:
                print(f"Frontend error: {stderr}")
    
    # Clean up any running processes
    if backend_process.poll() is None:
        backend_process.terminate()
        try:
            backend_process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            backend_process.kill()
    
    if frontend_process.poll() is None:
        frontend_process.terminate()
        try:
            frontend_process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            frontend_process.kill()
    
    return 1

if __name__ == "__main__":
    sys.exit(main())