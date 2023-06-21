FROM python:3.11-bullseye

# Install GEOS library
RUN apt-get update && apt-get install -y libgeos-dev

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt --timeout 100

# Install additional dependencies
RUN apt-get install -y liblzma-dev cmake

# Build GPT4All from source (required for GPT4All langchain bindings)
RUN cd /tmp && git clone --recurse-submodules https://github.com/nomic-ai/gpt4all && \
    cd gpt4all/gpt4all-backend/ && \
    mkdir build && cd build && \
    cmake .. && cmake --build . --parallel  && \
    cd ../../gpt4all-bindings/python && \
    pip3 install -e .

COPY . /code/

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "5050"]
