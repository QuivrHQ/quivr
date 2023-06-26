#!/bin/bash

# Check if gpt4all is already installed
if ! pip show gpt4all > /dev/null; then
    if [[ $PRIVATE == "True" ]]; then
        apt-get install -y liblzma-dev cmake

        cd /tmp && git clone --recurse-submodules https://github.com/nomic-ai/gpt4all
        cd gpt4all/gpt4all-backend/
        mkdir build && cd build
        cmake .. && cmake --build . --parallel
        cd ../../gpt4all-bindings/python
        pip3 install -e .
    fi
fi

# Move to the code directory
cd /code

# Start your app
uvicorn main:app --reload --host 0.0.0.0 --port 5050
