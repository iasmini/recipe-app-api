FROM python:3.7-alpine
MAINTAINER Iasmini Gomes

# recomendado quando está rodando python com container docker
# doesnt allow python to buffer the outputs
ENV PYTHONUNBUFFERED 1

# copy from local machine requirements to docker image to /requirements.txt
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# cria usuario somente para executar o projeto (por segurança, para não usar o root)
RUN adduser -D user
# switches to the created user
USER user