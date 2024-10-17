# Using a slim version for a smaller base image
FROM python:3.12.6-slim-bullseye@sha256:6fe70237cff8ad7c0a91b992cb7cb454187dfd2e3f08ce2d023907d76db8c287

ARG DEV_MODE
ENV DEV_MODE=$DEV_MODE

RUN apt-get clean && apt-get update && apt-get install -y wget curl

RUN ARCHITECTURE=$(uname -m) && \
    if [ "$ARCHITECTURE" = "x86_64" ]; then \
    wget https://github.com/supabase/cli/releases/download/v1.163.6/supabase_1.163.6_linux_amd64.deb && \
    dpkg -i supabase_1.163.6_linux_amd64.deb && \
    rm supabase_1.163.6_linux_amd64.deb; \
    elif [ "$ARCHITECTURE" = "aarch64" ]; then \
    wget https://github.com/supabase/cli/releases/download/v1.163.6/supabase_1.163.6_linux_arm64.deb && \
    dpkg -i supabase_1.163.6_linux_arm64.deb && \
    rm supabase_1.163.6_linux_arm64.deb; \
    fi && \
    rm -rf /var/lib/apt/lists/*

# TODO(@aminediro) : multistage build. Probably dont neet poetry once its built
# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false && \
    poetry config virtualenvs.in-project false

# Add Rust binaries to the PATH
ENV PATH="/root/.cargo/bin:${PATH}" \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_PATH=/code/api/.venv-docker

WORKDIR /code/api
COPY . /code/

RUN poetry install  && rm -rf $POETRY_CACHE_DIR

ENV PYTHONPATH=/code/api

EXPOSE 5050
