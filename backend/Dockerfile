# Using a slim version for a smaller base image
FROM python:3.11.6-slim-bullseye

ARG DEV_MODE
ENV DEV_MODE=$DEV_MODE

# Install GEOS library, Rust, and other dependencies, then clean up
RUN apt-get clean && apt-get update && apt-get install -y \
    libgeos-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    binutils \
    pandoc \
    curl \
    git \
    poppler-utils \
    tesseract-ocr \
    autoconf \
    automake \
    build-essential \
    libtool \
    python-dev \
    wget \
    # Additional dependencies for document handling
    libmagic-dev \
    poppler-utils \
    tesseract-ocr \
    libreoffice \
    libpq-dev \
    gcc \
    pandoc && \
    rm -rf /var/lib/apt/lists/*


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

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false


# Add Rust binaries to the PATH
ENV PATH="/root/.cargo/bin:${PATH}" \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /code

# Copy monorepo dependencies
# CORE
COPY core/pyproject.toml core/README.md core/poetry.lock  /code/core/
COPY core/quivr_core /code/core/quivr_core
# API
COPY api/pyproject.toml  api/poetry.lock api/README.md /code/api/
COPY api/quivr_api /code/api/quivr_api

COPY ./pyproject.toml ./poetry.lock* /code/

COPY ./ci-migration.sh /code/

COPY supabase /code/supabase/

# Run install
RUN poetry install --no-root --with dev,test && \
    playwright install --with-deps && \
    rm -rf $POETRY_CACHE_DIR


ENV PYTHONPATH=/code


EXPOSE 5050
