# Memory Leak Detection Automation

This repository contains scripts and tools to automate various tasks related to memory leak detection and deployment.

## `run.sh` Script Overview

The `run.sh` script automates the process of generating test cases, generating deployment scripts, running build and test commands, and validating memory leaks. It is designed to work with a specific repository and folder structure for efficient memory leak detection.

### Requirements

Before running the script, make sure you have the following:

- Python 3.x installed


### Usage

To run the script, execute the following command in your terminal:

```bash
./run.sh <repo_name> <folder_path> <file_name>
