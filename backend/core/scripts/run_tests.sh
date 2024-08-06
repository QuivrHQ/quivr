#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Constants
IMAGE_NAME="quivr-core-test"
IMAGE_TAG="latest"
DOCKERFILE="Dockerfile.test"
VOLUME_MAPPING="$PWD:/code"
TOX_DIR="/code/.tox-docker"
CMD="poetry run tox -p auto"

# Functions
build_image() {
    echo "Building Docker image..."
    docker build -f $DOCKERFILE -t $IMAGE_NAME:$IMAGE_TAG .
}

run_container() {
    echo "Running tests in Docker container..."
    docker run -it --rm \
        -e TOX_WORK_DIR=$TOX_DIR \
        -v $VOLUME_MAPPING \
        $IMAGE_NAME:$IMAGE_TAG $CMD
}

# Main script execution
build_image
run_container

echo "Tests completed successfully."
