#!/bin/bash

MODE=$1

IMAGE_NAME="bs_docker"

CONTAINER_NAME="bs_docker_container"

if [ "$MODE" == "debug" ]; then
    echo "Running in debug mode. Starting container in interactive mode..."
    docker run -p 5001:5001 -p 8000:8000 -it --rm  --name $CONTAINER_NAME $IMAGE_NAME /bin/bash
else
    echo "Running in normal mode. Starting container..."
    docker run -p 5001:5001 -p 8000:8000 -d --name $CONTAINER_NAME $IMAGE_NAME
fi