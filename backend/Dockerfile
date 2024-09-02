FROM python:3.11.6-slim-bullseye

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libgeos-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    binutils \
    pandoc \
    curl \
    git \
    poppler-utils \
    tesseract-ocr \
    libmagic-dev \
    libreoffice \
    libpq-dev \
    gcc \
    wget \
    && rm -rf /var/lib/apt/lists/*

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

COPY . .

RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

RUN playwright install --with-deps && \
    python -c "from unstructured.nlp.tokenize import download_nltk_packages; download_nltk_packages()" && \
    python -c "import nltk;nltk.download('punkt_tab'); nltk.download('averaged_perceptron_tagger_eng')"


ENV PYTHONPATH=/app

EXPOSE 5050
