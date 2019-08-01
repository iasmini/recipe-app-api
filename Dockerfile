FROM python:3.7-alpine
MAINTAINER Iasmini Gomes

# recomendado quando está rodando python com container docker
# doesnt allow python to buffer the outputs
ENV PYTHONUNBUFFERED 1

# copy from local machine requirements to docker image to /requirements.txt
COPY ./requirements.txt /requirements.txt
# --no-cache: dont store the registry index on our docker file to minimize the
# number of extra files and packages that are included in our docker container
RUN apk add --update --no-cache postgresql-client
# install necesseraly temporary packages while running requirements
# --virtual: sets up an alias for our dependencies to easily remove them later
RUN apk add --update --no-cache --virtual .tmp-buid-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
# deletes the temporary requirements
RUN apk del .tmp-buid-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# cria usuario somente para executar o projeto (por segurança, para não usar o
# root)
RUN adduser -D user
# switches to the created user
USER user