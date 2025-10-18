#!/bin/bash

# Code Consolidation Script
# This script consolidates all code files into a single text file for AI model input

# Output file
OUTPUT_FILE="consolidated_codebase.txt"

# Function to add file content with header
add_file_content() {
    local file_path="$1"
    local relative_path="${file_path#./}"
    
    echo "" >> "$OUTPUT_FILE"
    echo "========================================" >> "$OUTPUT_FILE"
    echo "FILE: $relative_path" >> "$OUTPUT_FILE"
    echo "========================================" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    
    # Check if file is binary
    if file "$file_path" | grep -q "text"; then
        cat "$file_path" >> "$OUTPUT_FILE"
    else
        echo "[BINARY FILE - Content not included]" >> "$OUTPUT_FILE"
    fi
    
    echo "" >> "$OUTPUT_FILE"
}

# Clear output file
> "$OUTPUT_FILE"

# Add project overview
echo "PROJECT: Intelligent Matchmaking System" >> "$OUTPUT_FILE"
echo "GENERATED: $(date)" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Add README files first
echo "========================================" >> "$OUTPUT_FILE"
echo "PROJECT DOCUMENTATION" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"

if [ -f "README.md" ]; then
    add_file_content "README.md"
fi

# Add documentation files
if [ -d "docs" ]; then
    find docs -name "*.md" -type f | sort | while read file; do
        add_file_content "$file"
    done
fi

echo "" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"
echo "BACKEND CODE" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"

# Backend Python files
if [ -d "backend" ]; then
    find backend -name "*.py" -type f | sort | while read file; do
        add_file_content "$file"
    done
    
    # Backend configuration files
    find backend -name "requirements.txt" -o -name "*.ini" -o -name "*.cfg" -o -name "*.yaml" -o -name "*.yml" -o -name "*.json" | sort | while read file; do
        add_file_content "$file"
    done
fi

echo "" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"
echo "MACHINE LEARNING CODE" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"

# ML Python files
if [ -d "ml" ]; then
    find ml -name "*.py" -type f | sort | while read file; do
        add_file_content "$file"
    done
fi

echo "" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"
echo "FRONTEND CODE" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"

# Frontend files
if [ -d "frontend" ]; then
    # Package.json and config files
    find frontend -name "package.json" -o -name "*.config.js" -o -name "*.json" | grep -v node_modules | sort | while read file; do
        add_file_content "$file"
    done
    
    # JavaScript and JSX files
    find frontend/src -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" | sort | while read file; do
        add_file_content "$file"
    done
    
    # CSS files
    find frontend -name "*.css" -o -name "*.scss" -o -name "*.sass" | sort | while read file; do
        add_file_content "$file"
    done
    
    # HTML files
    find frontend -name "*.html" | sort | while read file; do
        add_file_content "$file"
    done
fi

echo "" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"
echo "DATABASE SCRIPTS" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"

# Database files
if [ -d "database" ]; then
    find database -name "*.py" -o -name "*.js" -o -name "*.sql" -o -name "*.json" -o -name "*.sh" | sort | while read file; do
        add_file_content "$file"
    done
fi

echo "" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"
echo "CONFIGURATION FILES" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"

# Root level configuration files
find . -maxdepth 1 -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.ini" -o -name "*.cfg" -o -name "*.env*" -o -name "Dockerfile*" -o -name "docker-compose*" | sort | while read file; do
    add_file_content "$file"
done

# Add .gitignore if exists
if [ -f ".gitignore" ]; then
    add_file_content ".gitignore"
fi

echo "" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"
echo "PROJECT STRUCTURE" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Generate project structure
tree -a -I '__pycache__|node_modules|.git|*.pyc|*.log' >> "$OUTPUT_FILE" 2>/dev/null || {
    echo "Project structure (tree command not available):" >> "$OUTPUT_FILE"
    find . -type f -not -path "./.git/*" -not -path "./*/node_modules/*" -not -path "./*/__pycache__/*" | sort >> "$OUTPUT_FILE"
}

echo "" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"
echo "END OF CONSOLIDATED CODEBASE" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"

echo "Code consolidation complete! Output saved to: $OUTPUT_FILE"
echo "File size: $(du -h "$OUTPUT_FILE" | cut -f1)"
echo "Total lines: $(wc -l < "$OUTPUT_FILE")"

# Create a summary file
SUMMARY_FILE="consolidation_summary.txt"
> "$SUMMARY_FILE"

echo "CONSOLIDATION SUMMARY" >> "$SUMMARY_FILE"
echo "Generated: $(date)" >> "$SUMMARY_FILE"
echo "Output File: $OUTPUT_FILE" >> "$SUMMARY_FILE"
echo "File Size: $(du -h "$OUTPUT_FILE" | cut -f1)" >> "$SUMMARY_FILE"
echo "Total Lines: $(wc -l < "$OUTPUT_FILE")" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"
echo "Files Included:" >> "$SUMMARY_FILE"

# Count files by type
echo "Python files: $(find . -name "*.py" -not -path "./*/__pycache__/*" | wc -l)" >> "$SUMMARY_FILE"
echo "JavaScript files: $(find . -name "*.js" -o -name "*.jsx" -not -path "./*/node_modules/*" | wc -l)" >> "$SUMMARY_FILE"
echo "CSS files: $(find . -name "*.css" -o -name "*.scss" | wc -l)" >> "$SUMMARY_FILE"
echo "HTML files: $(find . -name "*.html" | wc -l)" >> "$SUMMARY_FILE"
echo "JSON files: $(find . -name "*.json" -not -path "./*/node_modules/*" | wc -l)" >> "$SUMMARY_FILE"
echo "Markdown files: $(find . -name "*.md" | wc -l)" >> "$SUMMARY_FILE"
echo "Configuration files: $(find . -name "*.config.js" -o -name "*.cfg" -o -name "*.ini" -o -name "*.yaml" -o -name "*.yml" | wc -l)" >> "$SUMMARY_FILE"

echo "Summary saved to: $SUMMARY_FILE"