# Using a slim version for a smaller base image
FROM python:3.11.6-slim-bullseye@sha256:0c1fbb294096d842ad795ee232d783cab436c90b034210fe894f2bb2f2be7626

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
    build-essential \
    # Additional dependencies for document handling
    libmagic-dev \
    poppler-utils \
    tesseract-ocr \
    libreoffice \
    libpq-dev \
    gcc \
    pandoc && \
    rm -rf /var/lib/apt/lists/* && apt-get clean

# Add Rust binaries to the PATH
ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /code

# Copy just the requirements first
COPY ./requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Increase timeout to wait for the new installation
RUN pip install --no-cache-dir -r requirements.txt --timeout 20000

RUN if [ "$DEV_MODE" = "true" ]; then pip install --no-cache debugpy --timeout 200; fi

# Copy the rest of the application
COPY . .

EXPOSE 5050

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5050", "--workers", "6"]