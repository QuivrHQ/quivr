FROM python:3.11.6-slim-bullseye

WORKDIR /app

# Install runtime dependencies
RUN apt-get clean && apt-get update && apt-get install -y \
    libgeos-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    binutils \
    curl \
    git \
    autoconf \
    automake \
    build-essential \
    libtool \
    python-dev \
    build-essential \
    wget \
    # Additional dependencies for document handling
    libmagic-dev \
    poppler-utils \
    tesseract-ocr \
    libreoffice \
    libpq-dev \
    gcc \
    libhdf5-serial-dev \
    pandoc && \
    rm -rf /var/lib/apt/lists/* && apt-get clean

# Install Supabase CLI
RUN ARCHITECTURE=$(uname -m) && \
    if [ "$ARCHITECTURE" = "x86_64" ]; then \
    wget https://github.com/supabase/cli/releases/download/v1.163.6/supabase_1.163.6_linux_amd64.deb && \
    dpkg -i supabase_1.163.6_linux_amd64.deb && \
    rm supabase_1.163.6_linux_amd64.deb; \
    elif [ "$ARCHITECTURE" = "aarch64" ]; then \
    wget https://github.com/supabase/cli/releases/download/v1.163.6/supabase_1.163.6_linux_arm64.deb && \
    dpkg -i supabase_1.163.6_linux_arm64.deb && \
    rm supabase_1.163.6_linux_arm64.deb; \
    fi

COPY requirements.lock  pyproject.toml README.md ./
COPY api/pyproject.toml api/README.md ./api/
COPY api/quivr_api/__init__.py ./api/quivr_api/__init__.py
COPY core/pyproject.toml core/README.md ./core/
COPY core/quivr_core/__init__.py ./core/quivr_core/__init__.py
COPY worker/pyproject.toml worker/README.md ./worker/
COPY worker/quivr_worker/__init__.py ./worker/quivr_worker/__init__.py
COPY worker/diff-assistant/pyproject.toml worker/diff-assistant/README.md ./worker/diff-assistant/
COPY worker/diff-assistant/quivr_diff_assistant/__init__.py ./worker/diff-assistant/quivr_diff_assistant/__init__.py

RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

RUN playwright install --with-deps && \
    python -c "from unstructured.nlp.tokenize import download_nltk_packages; download_nltk_packages()" && \
    python -c "import nltk;nltk.download('punkt_tab'); nltk.download('averaged_perceptron_tagger_eng')"


ENV PYTHONPATH=/app

COPY . .
EXPOSE 5050
