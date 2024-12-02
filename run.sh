#!/bin/bash

# Check if the correct number of arguments are passed
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <repo_name> <folder_path> <file_name>"
    exit 1
fi

# Assign arguments to variables
REPO_NAME=$1
FOLDER_PATH=$2
FILE_NAME=$3

TMP_DIR="tmp"

# Ensure tmp folder exists
if [ ! -d "$TMP_DIR" ]; then
  echo "Creating $TMP_DIR directory..."
  mkdir "$TMP_DIR"
fi
cd tmp
# Ensure repo folder exists
if [ ! -d "$REPO_NAME" ]; then
  echo "Creating $REPO_NAME directory..."
  mkdir "$REPO_NAME"
fi
cd ..

# Step 1: Generate test cases
echo "Generating test cases for $FILE_NAME in $FOLDER_PATH..."
python generate_test_cases.py $REPO_NAME $FOLDER_PATH $FILE_NAME

if [ $? -ne 0 ]; then
    echo "Exception in generating test cases. Exiting the code..."
    exit 1
fi

# Step 2: Generate deployment scripts
echo "Generating deployment scripts for repository $REPO_NAME in $FOLDER_PATH..."
python3 generate_deployment_scripts.py  $FOLDER_PATH $REPO_NAME

if [ $? -ne 0 ]; then
    echo "Exception in generating deployment scripts. Exiting the code..."
    exit 1
fi

# Step 3: You can run the code or further steps here
echo "Running the code or further steps..."
sh build_and_test.sh $FOLDER_PATH
# Step 4: Validate memory leak
echo "Validating memory leak..."
# You can add memory leak validation logic here
