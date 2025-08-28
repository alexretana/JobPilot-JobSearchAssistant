#!/bin/bash
# Script to run Playwright tests with a timeout

# Set a timeout of 5 minutes (300 seconds)
timeout 300 npx playwright test "$@"

# Check the exit code
if [ $? -eq 124 ]; then
    echo "Test execution timed out after 5 minutes"
    exit 1
else
    echo "Tests completed"
fi