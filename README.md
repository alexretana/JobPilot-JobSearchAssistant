# JP - JobPilot Career Assistant

A clean and maintainable career assistance platform focused on job searching and career networking.

## Documentation

- [Frontend Development Guide](frontend_development_guide.md) - Information about the frontend design and development workflow

## Running the Application

To run both the frontend and backend servers, you can use any of the following methods:

### Method 1: Using the original scripts
```bash
# On Windows
run_all.bat

# On Linux/Mac
./run_all.sh
```

Both servers will run as subprocesses. Press Ctrl+C to stop both servers.

To run both servers as background processes and return control to the terminal immediately:

```bash
# On Windows
run_all.bat --subprocess

# On Linux/Mac
./run_all.sh --subprocess
```

### Method 2: Using the new scripts (Recommended)
```bash
# On Windows - Start servers
start_dev_servers.bat

# On Windows - Stop servers
stop_dev_servers.bat
```

The new scripts start each server in its own window and verify that both are running correctly.

In subprocess mode, both servers run in the background, and you can continue using the terminal.

## Testing Server Startup

To verify that both servers start correctly, you can use the test scripts:

```bash
# On Windows
test_servers.bat

# On Linux/Mac
./test_servers.sh
```
