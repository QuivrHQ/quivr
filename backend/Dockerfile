# Using a slim version for a smaller base image
FROM python:3.11.6-slim-bullseye@sha256:0c1fbb294096d842ad795ee232d783cab436c90b034210fe894f2bb2f2be7626 AS base

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

# Add Rust binaries to the PATH
ENV PATH="/root/.cargo/bin:${PATH}"

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

WORKDIR /code

# Copy just the requirements first
COPY ./requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    playwright install --with-deps

# Copy the rest of the application
COPY . .

EXPOSE 5050

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5050", "--workers", "6"]