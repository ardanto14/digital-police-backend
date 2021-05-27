# syntax=docker/dockerfile:1
FROM python:3.6
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN apt update
RUN apt install ffmpeg libsm6 libxext6  -y
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/