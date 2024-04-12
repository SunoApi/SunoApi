# syntax=docker/dockerfile:1
FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 8051
CMD [ "nohup", "streamlit", "run", "main.py" ]

