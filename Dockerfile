FROM python:3.7-alpine
MAINTAINER Iasmini Gomes

# recomendado quando está rodando python com container docker
# doesnt allow python to buffer the outputs
ENV PYTHONUNBUFFERED 1

# copy from local machine requirements to docker image to /requirements.txt
COPY ./requirements.txt /requirements.txt
# --no-cache: dont store the registry index on our docker file to minimize the
# number of extra files and packages that are included in our docker container
# dependencias que nao serao excluidas apos a instalacao
# Pillow requires some packages to be installed using the pip package manager
# jpeg-dev, musl-dev zlib zlib-dev
RUN apk add --update --no-cache postgresql-client jpeg-dev
# install necesseraly temporary packages while running requirements
# --virtual: sets up an alias for our dependencies to easily remove them later
# dependencias que serao excluidas apos a instalacao (permanecem no container)
RUN apk add --update --no-cache --virtual .tmp-buid-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
# deletes the temporary requirements
RUN apk del .tmp-buid-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# place where we can store the static and media files within our container
# without getting any permission arrows.
# -p: se /vol nao existe, cria. se /web nao existe, cria
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

# cria usuario somente para executar o projeto (por segurança, para não usar o
# root)
RUN adduser -D user
# assigns ownerhip off all of directories within the volume directory to user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
# switches to the created user
USER user
