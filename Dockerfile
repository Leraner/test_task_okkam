FROM python:3.10

WORKDIR /src

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY ./requirements.txt /src/requirements.txt
COPY . /src/

RUN pip install -r /src/requirements.txt