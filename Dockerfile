# pull official base image
FROM python:3.8.0

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN ln -s /usr/lib/x86_64-linux-gnu/libz.so /lib/
RUN ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /lib/

RUN pip install -U pip
RUN pip install --no-binary pillow pillow

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/
