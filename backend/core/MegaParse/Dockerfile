# Using a slim version for a smaller base image
FROM python:3.12.7-slim-bullseye@sha256:dbdf1a8e375131679547183a70bdb4f9c512946a4ae42de172d59b151c3da5b7

# Install GEOS library, Rust, and other dependencies, then clean up
RUN apt-get clean && apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr 

WORKDIR /code

# Upgrade pip and install dependencies
RUN pip install megaparse

# You can run the application with the following command:
# docker run -it megaparse_image python your_script.py

