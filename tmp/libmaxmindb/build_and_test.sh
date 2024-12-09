#!/bin/bash

# Build Docker Image
docker build -t c_project .

# Run Docker Container
docker run -it -d --name c_project_container c_project 

# Execute Tests
docker exec -it c_project_container make check 

# Check for memory leaks
docker exec -it c_project_container valgrind --leak-check=full ./memory_leak_unit_test

# Copy logs from the Docker Container
docker cp c_project_container:/home/soumya/Automation/git_repos/libmaxminddb/memory_leak.log ./tmp/libmaxmindb

# Clean Up
docker rm -f c_project_container
docker image rm c_project