#!/bin/bash
# install-advanced-precommit.sh
# Helper script to install the advanced pre-commit hook with retry logic

echo "🔧 Installing advanced pre-commit hook..."

# First, ensure pre-commit is installed normally
if ! pre-commit install; then
    echo "❌ Failed to install pre-commit. Make sure pre-commit is available."
    exit 1
fi

# Backup the original hook
if [ -f ".git/hooks/pre-commit" ]; then
    cp ".git/hooks/pre-commit" ".git/hooks/pre-commit-original"
    echo "✅ Backed up original pre-commit hook to pre-commit-original"
else
    echo "❌ No pre-commit hook found. Run 'pre-commit install' first."
    exit 1
fi

# Create our advanced wrapper
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
# .git/hooks/pre-commit
# Advanced pre-commit wrapper with retry logic and selective file unstaging
# This hook attempts to run pre-commit up to 3 times, re-adding files between attempts
# If all attempts fail, it tries to unstage only the problematic files

MAX_RETRIES=2
COUNT=0

# Use Windows temp directory if on Windows, otherwise use /tmp
if [ -n "$TEMP" ]; then
    TEMP_DIR="$TEMP"
else
    TEMP_DIR="/tmp"
fi

TEMP_LOG="$TEMP_DIR/pre-commit-output.log"
FAILED_FILES="$TEMP_DIR/pre-commit-failed-files.log"

# Colors for better output (if supported)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m' # No Color
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    NC=''
fi

echo "${BLUE}🔍 Starting pre-commit validation...${NC}"

# Function to extract failed files from pre-commit output
extract_failed_files() {
    local log_file="$1"
    local failed_files_list="$2"
    
    # Clear the failed files list
    > "$failed_files_list"
    
    # Parse pre-commit output to find files that failed
    if [ -f "$log_file" ]; then
        # Pattern 1: Files listed after "Files were modified by this hook"
        grep -A 20 "Files were modified by this hook" "$log_file" 2>/dev/null | grep "^  " | sed 's/^  //' >> "$failed_files_list" 2>/dev/null || true
        
        # Pattern 2: Files mentioned in error lines (filename:line:column format)
        grep -E "^[^:]+:[0-9]+:[0-9]+" "$log_file" 2>/dev/null | cut -d: -f1 >> "$failed_files_list" 2>/dev/null || true
        
        # Pattern 3: Black "would reformat" messages
        grep "would reformat" "$log_file" 2>/dev/null | sed 's/would reformat //' >> "$failed_files_list" 2>/dev/null || true
        
        # Pattern 4: Ruff error format
        grep -E "Found [0-9]+ error" "$log_file" -A 10 2>/dev/null | grep -E "\\.py:" | cut -d: -f1 >> "$failed_files_list" 2>/dev/null || true
        
        # Pattern 5: Generic file paths in the output
        grep -E "\\.(py|js|ts|json|yaml|yml|md|txt|toml)( |$)" "$log_file" 2>/dev/null | grep -oE "[^ ]*\\.(py|js|ts|json|yaml|yml|md|txt|toml)" >> "$failed_files_list" 2>/dev/null || true
        
        # Remove duplicates and empty lines, and ensure files actually exist
        if [ -s "$failed_files_list" ]; then
            sort "$failed_files_list" | uniq | while IFS= read -r file; do
                if [ -n "$file" ] && [ -f "$file" ]; then
                    echo "$file"
                fi
            done > "${failed_files_list}.tmp"
            mv "${failed_files_list}.tmp" "$failed_files_list" 2>/dev/null || true
        fi
    fi
}

# Function to unstage specific files
unstage_files() {
    local files_list="$1"
    local count=0
    
    if [ -f "$files_list" ] && [ -s "$files_list" ]; then
        echo "${YELLOW}📤 Unstaging problematic files:${NC}"
        while IFS= read -r file; do
            if [ -n "$file" ] && git diff --cached --name-only | grep -Fq "$file"; then
                echo "  - $file"
                git reset HEAD "$file" 2>/dev/null || true
                count=$((count + 1))
            fi
        done < "$files_list"
        
        if [ $count -eq 0 ]; then
            echo "${YELLOW}⚠️  No matching staged files found to unstage.${NC}"
            return 1
        else
            echo "${GREEN}✅ Unstaged $count problematic files.${NC}"
            return 0
        fi
    else
        echo "${YELLOW}⚠️  Could not identify specific failed files.${NC}"
        return 1
    fi
}

# Main retry loop
while [ $COUNT -le $MAX_RETRIES ]
do
    echo "${BLUE}🚀 Running pre-commit (attempt $((COUNT+1))/$(($MAX_RETRIES+1)))...${NC}"
    
    # Run the original pre-commit hook and capture output
    if .git/hooks/pre-commit-original 2>&1 | tee "$TEMP_LOG"; then
        echo "${GREEN}✅ Pre-commit checks passed on attempt $((COUNT+1))!${NC}"
        # Cleanup temp files
        rm -f "$TEMP_LOG" "$FAILED_FILES" 2>/dev/null || true
        exit 0
    fi
    
    STATUS=$?
    echo "${RED}❌ Pre-commit failed on attempt $((COUNT+1)) (exit code: $STATUS)${NC}"
    
    # If this isn't the last attempt, try to fix and retry
    if [ $COUNT -lt $MAX_RETRIES ]; then
        echo "${YELLOW}🔄 Extracting failed files and re-adding for retry...${NC}"
        
        # Extract failed files for potential later use
        extract_failed_files "$TEMP_LOG" "$FAILED_FILES"
        
        # Re-add all modified files (some hooks may have fixed formatting)
        echo "${BLUE}📝 Re-adding modified files...${NC}"
        git add -u 2>/dev/null || true
        
        echo "${YELLOW}⏳ Waiting 1 second before retry...${NC}"
        sleep 1
    fi
    
    COUNT=$((COUNT+1))
done

# All retries failed
echo "${RED}❌ Pre-commit still failing after $(($MAX_RETRIES+1)) attempts.${NC}"
echo "${YELLOW}🔍 Analyzing failures...${NC}"

# Extract failed files from the last run
extract_failed_files "$TEMP_LOG" "$FAILED_FILES"

# Try to unstage only the problematic files
if unstage_files "$FAILED_FILES"; then
    echo "${GREEN}✅ Successfully unstaged problematic files.${NC}"
    echo "${BLUE}💡 You can now commit the remaining staged files, and fix the unstaged ones separately.${NC}"
    
    # Show what files are still staged
    staged_files=$(git diff --cached --name-only)
    if [ -n "$staged_files" ]; then
        echo "${GREEN}📋 Files still staged for commit:${NC}"
        echo "$staged_files" | sed 's/^/  ✓ /'
    fi
    
    # Show what files were unstaged
    if [ -s "$FAILED_FILES" ]; then
        echo "${YELLOW}📋 Files unstaged due to failures:${NC}"
        cat "$FAILED_FILES" | sed 's/^/  ❌ /'
    fi
    
else
    echo "${RED}⚠️  Could not identify specific failed files.${NC}"
    echo "${YELLOW}🤔 Choose your next action:${NC}"
    echo "  1. Run: ${BLUE}git reset${NC} to unstage ALL files"
    echo "  2. Run: ${BLUE}git commit --no-verify${NC} to bypass pre-commit"
    echo "  3. Fix issues manually and try again"
    
    # Don't auto-unstage everything - let the user decide
fi

# Show the last few lines of the log for context
if [ -f "$TEMP_LOG" ]; then
    echo "${BLUE}📄 Last few lines of pre-commit output:${NC}"
    tail -10 "$TEMP_LOG" 2>/dev/null || true
fi

# Cleanup temp files
rm -f "$TEMP_LOG" "$FAILED_FILES" 2>/dev/null || true

echo "${RED}❌ Commit blocked due to pre-commit failures.${NC}"
exit 1
EOF

# Make the hook executable
chmod +x .git/hooks/pre-commit

echo "✅ Advanced pre-commit hook installed successfully!"
echo ""
echo "🔍 Features:"
echo "  • Retries pre-commit up to 3 times (auto-fixes formatting issues)"
echo "  • Intelligently unstages only problematic files if all retries fail"
echo "  • Colorized output with helpful guidance"
echo "  • Preserves files that pass validation for commit"
echo ""
echo "💡 To restore the original pre-commit hook:"
echo "   cp .git/hooks/pre-commit-original .git/hooks/pre-commit"
