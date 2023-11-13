# First stage: Build environment
FROM python:3.11-slim-bullseye as builder

ARG DEV_MODE
ENV DEV_MODE=$DEV_MODE

# Install GEOS library, Rust, and other build-time dependencies
RUN apt-get update && apt-get install -y \
    libgeos-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    pandoc \
    binutils \
    curl \
    git \
    build-essential && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    rm -rf /var/lib/apt/lists/* && apt-get clean

# Add Rust binaries to the PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Create a virtual environment and activate it
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

WORKDIR /code

# Copy just the requirements first
COPY ./requirements.txt .

# Upgrade pip and install requirements
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt --timeout 200

# Install development tools if in DEV_MODE
RUN if [ "$DEV_MODE" = "true" ]; then pip install --no-cache debugpy --timeout 200; fi



FROM python:3.11-slim-bullseye as runtime

ARG DEV_MODE
ENV DEV_MODE=$DEV_MODE

# Create and activate the virtual environment
ENV PATH="/venv/bin:$PATH"

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    pandoc \
    binutils && \
    rm -rf /var/lib/apt/lists/* && apt-get clean

WORKDIR /code

# Copy the virtual environment from the builder stage
COPY --from=builder /venv /venv

# Copy the rest of the application
COPY . .

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "5050", "--workers", "6"]
