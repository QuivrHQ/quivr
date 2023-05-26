# Dockerfile for frontend
FROM node:14.17.6-alpine
WORKDIR /app
COPY ./frontend/ ./
RUN npm install
EXPOSE 3000
CMD ["npm", "run", "dev"]

# Dockerfile for backend
FROM python:3.9.6-alpine
WORKDIR /code
COPY ./backend/ ./
RUN pip install -r requirements.txt
EXPOSE 5050
CMD ["python", "app.py"]
