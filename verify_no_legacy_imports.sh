#!/bin/bash
# Script to verify that no legacy API imports remain in the frontend components

echo "Checking for legacy API imports in frontend components..."

# Search for any imports of the old API modules
LEGACY_IMPORTS=$(grep -r "import.*Api" frontend/src/components --include="*.tsx" | grep -v "ApiService")

if [ -z "$LEGACY_IMPORTS" ]; then
    echo "✅ No legacy API imports found in frontend components"
    exit 0
else
    echo "❌ Legacy API imports still found:"
    echo "$LEGACY_IMPORTS"
    exit 1
fi