# pull official base image
FROM python:3.8.0

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONUNBUFFERED 1

# update and upgrade apt
RUN apt-get update && apt-get -y upgrade

# add requirements
ADD requirements.txt .

# install  requirements
RUN python -m venv /venv \
    && /venv/bin/pip install --upgrade pip \
    && /venv/bin/pip install -r requirements.txt

# add entrypoint
ADD entrypoint.dev.sh .

# add the project
ADD . .

# run entrypoint
ENTRYPOINT ["/usr/src/app/entrypoint.dev.sh"]
