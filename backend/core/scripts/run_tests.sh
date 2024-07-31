#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Constants
IMAGE_NAME="quivr-core-test"
IMAGE_TAG="latest"
DOCKERFILE="Dockerfile.test"
VOLUME_MAPPING="$PWD:/code"
CMD=" poetry run tox"

# Functions
build_image() {
    echo "Building Docker image..."
    docker build -f $DOCKERFILE -t $IMAGE_NAME:$IMAGE_TAG .
}

run_container() {
    echo "Running tests in Docker container..."
export 
    docker run -it --rm -e TOX_WORK_DIR=/code/.tox-docker -v $VOLUME_MAPPING $IMAGE_NAME:$IMAGE_TAG $CMD
}

# Main script execution
build_image
run_container

echo "Tests completed successfully."
