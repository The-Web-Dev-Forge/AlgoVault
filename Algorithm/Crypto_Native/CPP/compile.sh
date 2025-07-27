#!/bin/bash

# C++ Cryptographic Algorithms Compilation Script
# Compiles all cryptographic implementations in the CPP directory

echo "Compiling C++ Cryptographic Algorithms..."
echo "========================================"

# Function to compile a single C++ file
compile_cpp() {
    local source_file=$1
    local executable_name=${source_file%.cpp}
    
    echo "Compiling $source_file..."
    if g++ -std=c++11 -O2 -Wall -Wextra "$source_file" -o "$executable_name"; then
        echo "✓ Successfully compiled $executable_name"
        chmod +x "$executable_name"
    else
        echo "✗ Failed to compile $source_file"
        return 1
    fi
}

# Compile all C++ files
files_compiled=0
files_failed=0

for cpp_file in *.cpp; do
    if [[ -f "$cpp_file" ]]; then
        if compile_cpp "$cpp_file"; then
            ((files_compiled++))
        else
            ((files_failed++))
        fi
        echo ""
    fi
done

# Summary
echo "========================================"
echo "Compilation Summary:"
echo "✓ Successfully compiled: $files_compiled files"
if [[ $files_failed -gt 0 ]]; then
    echo "✗ Failed to compile: $files_failed files"
fi

echo ""
echo "Available executables:"
for exe in *.exe $(find . -maxdepth 1 -type f -executable ! -name "*.sh" ! -name ".*"); do
    if [[ -f "$exe" && -x "$exe" ]]; then
        echo "  - $exe"
    fi
done

echo ""
echo "Compilation completed!"