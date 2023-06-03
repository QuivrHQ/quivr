FROM python:3.11-buster

# Install GEOS library
RUN apt-get update && apt-get install -y libgeos-dev

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt --timeout 100

COPY . /code/

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "5050"]