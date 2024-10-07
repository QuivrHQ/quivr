# Using a slim version for a smaller base image
FROM python:3.11.6-slim-bullseye@sha256:0c1fbb294096d842ad795ee232d783cab436c90b034210fe894f2bb2f2be7626

# Install GEOS library, Rust, and other dependencies, then clean up
RUN apt-get clean && apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr 

WORKDIR /code

# Upgrade pip and install dependencies
RUN pip install megaparse

# You can run the application with the following command:
# docker run -it megaparse_image python your_script.py

