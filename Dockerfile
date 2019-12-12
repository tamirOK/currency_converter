FROM python:3.7-slim

COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1

WORKDIR /currency_converter/
