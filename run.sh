#!/bin/bash

# Check if the correct number of arguments are passed
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <repo_name> <folder_path> <file_name> <fixed_code_file>"
    exit 1
fi

# Assign arguments to variables
REPO_NAME=$1
FOLDER_PATH=$2
FILE_NAME=$3
FIXED_CODE_FILE=$4

TMP_DIR="tmp"

echo "Folder Path: $FOLDER_PATH"

# Ensure tmp folder exists
if [ ! -d "$TMP_DIR" ]; then
  echo "Creating $TMP_DIR directory..."
  mkdir "$TMP_DIR"
fi

# Ensure repo folder exists
if [ ! -d "$TMP_DIR/$REPO_NAME" ]; then
  echo "Creating $REPO_NAME directory inside tmp..."
  mkdir "$TMP_DIR/$REPO_NAME"
fi

# Retry limit
MAX_ATTEMPTS=3
attempt=1

while [ $attempt -le $MAX_ATTEMPTS ]; do
    echo "Attempt $attempt of $MAX_ATTEMPTS..."

    # Step 1: Generate test cases
    echo "Generating test cases for $FILE_NAME in $FOLDER_PATH..."
    python3 generate_test_cases.py "$REPO_NAME" "$FOLDER_PATH" "$FILE_NAME"

    if [ $? -ne 0 ]; then
        echo "Exception in generating test cases. Exiting..."
        exit 1
    fi

    # Step 2: Generate deployment scripts
    echo "Generating deployment scripts for $REPO_NAME..."
    python3 generate_deployment_scripts.py "$FOLDER_PATH" "$REPO_NAME"

    if [ $? -ne 0 ]; then
        echo "Exception in generating deployment scripts. Exiting..."
        exit 1
    fi

    # Step 3: Build and run tests
    echo "Running build and test scripts..."
    sh build_and_test.sh "$FOLDER_PATH"

    # Step 4: Validate memory leak
    echo "Validating memory leak..."
    result=$(python3 validate_memory_leak.py "./tmp/$REPO_NAME/memory_leak.log" "$FOLDER_PATH/$FILE_NAME" "./tmp/$REPO_NAME/generated_test_cases.py" "$FIXED_CODE_FILE")

    # If validation succeeds, exit the script
    if [ "$result" -ne -1 ]; then
        echo "Memory leak validation passed. Return value: $result"
        echo "Successfully generated and validated test cases. Exiting..."
        exit 0
    else
        echo "Memory leak validation failed. Retrying..."
        attempt=$((attempt + 1))
    fi
done

# If the loop completes without success
echo "Maximum attempts ($MAX_ATTEMPTS) reached. Memory leak is not reproduced...."
exit 1
