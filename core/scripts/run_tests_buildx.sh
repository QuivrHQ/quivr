#!/bin/bash

set -e

# Constants
IMAGE_NAME="quivr-core-test"
IMAGE_TAG="latest"
DOCKERFILE="Dockerfile.test"
VOLUME_MAPPING="$PWD:/code"
CMD="poetry run tox"
PLATFORM="linux/amd64"
BUILDER_NAME="amd64_builder"

# Functions
build_image() {
    echo "Building Docker image for $PLATFORM..."
    EXISTING_BUILDER=$(docker buildx ls | grep -w $BUILDER_NAME)

    # Create the builder if it doesn't exist
    if [ -z "$EXISTING_BUILDER" ]; then
        echo "Creating builder: $BUILDER_NAME"
        docker buildx create --use --name $BUILDER_NAME --platform $PLATFORM
    else
        echo "Builder $BUILDER_NAME already exists. Skipping creation."
    fi

    docker buildx build --platform $PLATFORM -f $DOCKERFILE -t $IMAGE_NAME:$IMAGE_TAG --load .
}

run_container() {
    echo "Running tests in Docker container..."
    docker run -it --rm --platform $PLATFORM -v $VOLUME_MAPPING $IMAGE_NAME:$IMAGE_TAG $CMD
}

# Main script execution
build_image
run_container

echo "Tests completed successfully."