FROM python:3.11.6-slim-bullseye AS BUILDER

ARG DEV_MODE
ENV DEV_MODE=$DEV_MODE

# Install GEOS library, Rust, and other dependencies, then clean up
RUN apt-get clean && apt-get update && apt-get install -y \
    libgeos-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    binutils \
    curl \
    git \
    gcc \
    autoconf \
    automake \
    build-essential \
    libtool \
    python-dev \
    wget \
    # Additional dependencies for document handling
    libmagic-dev \
    tesseract-ocr \
    poppler-utils \
    tesseract-ocr \
    libreoffice \
    libpq-dev \
    pandoc && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /code/worker
# Add Rust binaries to the PATH
ENV PATH="/root/.cargo/bin:${PATH}" \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_PATH=/code/worker/.venv-docker

COPY . /code/



# Cache playwright dependency
RUN poetry run pip install playwright && playwright install --with-deps

# Run install
RUN poetry install  && rm -rf $POETRY_CACHE_DIR

RUN poetry run python -c "from unstructured.nlp.tokenize import download_nltk_packages; download_nltk_packages()"

ENV PYTHONPATH=/code/worker
