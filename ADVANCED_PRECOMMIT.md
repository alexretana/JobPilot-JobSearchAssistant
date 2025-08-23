# 🚀 Advanced Pre-Commit Hook System

This project uses an enhanced pre-commit hook system that provides intelligent retry logic and selective file unstaging capabilities.

## 🎯 Features

### ✨ **Smart Retry Logic**
- **3 Attempts**: Automatically retries pre-commit up to 3 times
- **Auto-Fix Detection**: Recognizes when formatters (Black, Ruff) fix issues automatically
- **Progressive Recovery**: Re-adds modified files between attempts

### 🎯 **Selective File Management**
- **Intelligent Unstaging**: Only unstages files that actually failed validation
- **Preserve Clean Files**: Files that pass validation remain staged for commit
- **Smart Pattern Detection**: Analyzes pre-commit output to identify problematic files

### 🎨 **Enhanced User Experience**
- **Colorized Output**: Clear visual indicators for different states
- **Helpful Guidance**: Provides actionable next steps when issues occur
- **Progress Tracking**: Shows attempt numbers and status clearly

## 🔧 How It Works

### Normal Flow (Success)
```
🔍 Starting pre-commit validation...
🚀 Running pre-commit (attempt 1/3)...
✅ Pre-commit checks passed on attempt 1!
[Commit proceeds normally]
```

### Auto-Fix Flow (Formatting Issues)
```
🔍 Starting pre-commit validation...
🚀 Running pre-commit (attempt 1/3)...
❌ Pre-commit failed on attempt 1 (exit code: 1)
🔄 Extracting failed files and re-adding for retry...
📝 Re-adding modified files...
⏳ Waiting 1 second before retry...
🚀 Running pre-commit (attempt 2/3)...
✅ Pre-commit checks passed on attempt 2!
[Commit proceeds with auto-fixed files]
```

### Selective Unstaging Flow (Persistent Issues)
```
🔍 Starting pre-commit validation...
🚀 Running pre-commit (attempt 1/3)...
❌ Pre-commit failed on attempt 1 (exit code: 1)
[... retries ...]
❌ Pre-commit still failing after 3 attempts.
🔍 Analyzing failures...
📤 Unstaging problematic files:
  - problematic_file.py
  - another_issue.py
✅ Successfully unstaged 2 problematic files.
💡 You can now commit the remaining staged files, and fix the unstaged ones separately.

📋 Files still staged for commit:
  ✓ good_file.py
  ✓ test_file.py

📋 Files unstaged due to failures:
  ❌ problematic_file.py
  ❌ another_issue.py
```

## 🛠️ Installation

The advanced hook is automatically installed. If you need to reinstall it:

```bash
# Run the helper script
./install-advanced-precommit.sh
```

Or manually:
```bash
# Backup and replace the hook
mv .git/hooks/pre-commit .git/hooks/pre-commit-original
# Then copy the advanced hook content to .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

## 📋 Supported Hook Patterns

The system can intelligently detect failures from:

- **Black**: "would reformat" messages, file modification indicators
- **Ruff**: Error format with file:line:column patterns  
- **Pre-commit**: "Files were modified by this hook" messages
- **Generic**: File paths in error output
- **Trailing Whitespace**: File modification patterns
- **End of File Fixer**: File modification patterns

## 🔄 Configuration

### Retry Settings
```bash
MAX_RETRIES=2  # Total of 3 attempts (0, 1, 2)
```

### File Detection Patterns
The hook uses multiple patterns to detect failed files:
1. Post-hook modification lists
2. Error line formats (file:line:column)
3. Formatter-specific messages
4. Generic file path extraction

### Temporary Files
- **Windows**: Uses `$TEMP` directory
- **Unix/Linux**: Uses `/tmp` directory
- **Files**: `pre-commit-output.log`, `pre-commit-failed-files.log`

## 🚨 Troubleshooting

### Hook Not Running
```bash
# Verify hook exists and is executable
ls -la .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Restore Original Hook
```bash
cp .git/hooks/pre-commit-original .git/hooks/pre-commit
```

### Bypass Hook (Emergency)
```bash
git commit --no-verify -m "Emergency commit"
```

### Manual Unstaging
```bash
# If selective unstaging fails, manually unstage all
git reset

# Or unstage specific files
git reset HEAD filename.py
```

## 💡 Best Practices

### 1. **Let Auto-Fixes Work**
Most formatting issues (Black, Ruff auto-fixes) will be resolved automatically on retry.

### 2. **Review Unstaged Files**
When files are automatically unstaged, review and fix them before the next commit:
```bash
# Check what was unstaged
git status

# Fix issues and re-add
git add fixed_file.py
```

### 3. **Commit Incrementally**
Take advantage of selective unstaging to commit clean files first:
```bash
# Commit the files that passed
git commit -m "Add clean implementations"

# Fix and commit problematic files separately
git add fixed_file.py
git commit -m "Fix linting issues in problematic file"
```

### 4. **Monitor Hook Output**
Pay attention to the detailed output - it provides valuable information about what failed and why.

## 🔍 Advanced Usage

### Testing the Hook
```bash
# Create a file with formatting issues
echo "def bad_format( ):pass" > test.py
git add test.py
git commit -m "Test hook"
# Should auto-fix on retry
```

### Debugging Hook Issues
```bash
# Run pre-commit manually to see detailed output
.venv\Scripts\activate && pre-commit run --all-files
```

### Customizing Patterns
Edit `.git/hooks/pre-commit` and modify the `extract_failed_files()` function to add custom failure detection patterns.

---

## 🎉 Benefits

- **🚀 Faster Development**: Auto-fixes reduce manual formatting work
- **🎯 Selective Commits**: Commit clean code while fixing problematic files separately  
- **🛡️ Code Quality**: Maintains high standards while being developer-friendly
- **⚡ Intelligent Recovery**: Learns from failures and guides next steps
- **🎨 Great UX**: Clear feedback and actionable guidance

This advanced system transforms pre-commit from a potential roadblock into an intelligent development assistant! 🎯
