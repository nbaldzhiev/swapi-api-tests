# syntax=docker/dockerfile:1

FROM python:3.11.3-slim-bullseye

WORKDIR /swapi-api-tests-app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD pytest