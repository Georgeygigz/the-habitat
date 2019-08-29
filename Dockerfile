FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /habitat
WORKDIR /habitat

COPY requirements.txt /habitat/
RUN pip install -r requirements.txt
COPY . /habitat/
