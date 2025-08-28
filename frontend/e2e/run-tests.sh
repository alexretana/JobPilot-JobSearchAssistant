#!/bin/bash
# Test runner script that shows progress and prevents hanging

echo "Starting Playwright tests..."
echo "============================"

# Run tests with timeout and capture output
timeout 300s npx playwright test --reporter=list "$@" 2>&1 | tee test-output.log

# Check the exit code
EXIT_CODE=$?
if [ $EXIT_CODE -eq 124 ]; then
    echo ""
    echo "❌ Test execution timed out after 5 minutes"
    echo "This is likely because the tests were hanging"
    echo ""
    echo "To troubleshoot:"
    echo "1. Check that all test files exist"
    echo "2. Verify test page files are correctly formatted"
    echo "3. Try running individual tests instead of the full suite"
    echo ""
    exit 1
elif [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
    echo ""
else
    echo ""
    echo "❌ Some tests failed"
    echo "Check test-output.log for details"
    echo ""
fi

exit $EXIT_CODE