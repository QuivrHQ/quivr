# Using a slim version for a smaller base image
FROM python:3.11-slim-bullseye

# Install GEOS library and clean up in one step
RUN apt-get update && apt-get install -y libgeos-dev pandoc binutils && \
    rm -rf /var/lib/apt/lists/* && apt-get clean

WORKDIR /code

# Copy just the requirements first
COPY ./requirements.txt .


# Increase timeout might not be necessary but is retained as in original
RUN pip install --no-cache-dir -r requirements.txt --timeout 100

# Copy the rest of the application
COPY . .

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "5050"]
