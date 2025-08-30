@echo off
REM Script to verify that no legacy API imports remain in the frontend components

echo Checking for legacy API imports in frontend components...

REM Search for any imports of the old API modules
findstr /s /i /m "import.*Api" frontend\src\components\*.tsx | findstr /v "ApiService" > temp_legacy_imports.txt

if %errorlevel% equ 1 (
    echo ✅ No legacy API imports found in frontend components
    del temp_legacy_imports.txt >nul 2>&1
    exit /b 0
) else (
    echo ❌ Legacy API imports still found:
    type temp_legacy_imports.txt
    del temp_legacy_imports.txt >nul 2>&1
    exit /b 1
)