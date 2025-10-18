# Code Consolidation Scripts

This directory contains multiple scripts to consolidate your codebase into a single text file for AI model input.

## Available Scripts

### 1. `consolidate_code_quick.py` (⭐ RECOMMENDED)
**Quick Python script** - Fast and focused consolidation

**Usage:**
```bash
python consolidate_code_quick.py
```

**Output:** `consolidated_codebase_quick.txt` (~0.4 MB)

**Features:**
- Focuses on main application code
- Excludes unnecessary files
- Fast execution
- Perfect size for AI models
- Includes: Backend, Frontend, ML, Database code

### 2. `consolidate_code.py` 
**Full Python script** - Comprehensive but may be too large

**Usage:**
```bash
python consolidate_code.py
```

**Output:** `consolidated_codebase.txt` (~186 MB - too large!)

**Features:**
- Includes ALL files (may be overwhelming)
- Cross-platform compatibility
- Smart text file detection
- Handles encoding issues gracefully

### 2. `consolidate_code.sh`
**Bash shell script** - Works on Linux, macOS, and Windows with WSL/Git Bash

**Usage:**
```bash
chmod +x consolidate_code.sh
./consolidate_code.sh
```

### 3. `consolidate_code.bat`
**Windows batch file** - Works on Windows Command Prompt

**Usage:**
```cmd
consolidate_code.bat
```

## Output Files

Both scripts generate two files:

1. **`consolidated_codebase.txt`** - Contains all your code files with clear headers
2. **`consolidation_summary.txt`** - Contains statistics about the consolidation

## What Gets Included

The scripts will include:
- All Python files (`.py`)
- All JavaScript/TypeScript files (`.js`, `.jsx`, `.ts`, `.tsx`)
- All HTML/CSS files (`.html`, `.css`, `.scss`)
- Configuration files (`.json`, `.yaml`, `.yml`, `.ini`, `.cfg`)
- Documentation files (`.md`, `.txt`)
- Database scripts (`.sql`, `.sh`)
- README files
- Other text-based files

## What Gets Excluded

- Binary files (images, executables, etc.)
- Cache directories (`__pycache__`, `node_modules`, `.git`)
- Log files and temporary files
- Build artifacts

## File Structure in Output

The consolidated file is organized into sections:
1. Project Documentation (README files)
2. Documentation Files (docs folder)
3. Backend Code (Python files)
4. Machine Learning Code (ML folder)
5. Frontend Code (JS/React files)
6. Database Scripts
7. Configuration Files

## Tips for AI Model Usage

When sharing the consolidated file with an AI model:

1. **Mention the project type**: "This is a full-stack web application with Python backend, React frontend, and MongoDB database"

2. **Specify your request clearly**: What you want the AI to help you with

3. **File size consideration**: The consolidated file might be large. If it exceeds token limits, you can:
   - Use only specific sections
   - Split into multiple parts
   - Focus on particular components

## Example Usage

```bash
# Run the Python script (recommended)
python consolidate_code.py

# Check the output
ls -la consolidated_codebase.txt consolidation_summary.txt

# View the summary
cat consolidation_summary.txt
```

The consolidated file will be ready to share with any AI model for code analysis, review, or development assistance!