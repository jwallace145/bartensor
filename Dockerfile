# pull official base image
FROM ubuntu:18.04

ENV PYTHONUNBUFFERED 1

# update and upgrade apt
RUN apt-get update \
    && apt-get -y upgrade

# set working directory
WORKDIR /usr/src/app

# add requirements
ADD requirements.txt .

# install dependencies
RUN apt-get install -y apt-utils vim curl apache2 apache2-utils lynx \
    && apt-get install -y python3 libapache2-mod-wsgi-py3 \
    && apt-get install -y python3-pip \
    && ln /usr/bin/python3 /usr/bin/python \
    && ln /usr/bin/pip3 /usr/bin/pip \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# add apache2 configs
ADD bartensor.dev.conf  /etc/apache2/sites-available/000-default.conf

# add entrypoint script
ADD entrypoint.dev.sh .

# add the project
ADD . .

# expose port 80
EXPOSE 80

# grant execute permissions to entrypoint script
RUN ["chmod", "+x", "/usr/src/app/entrypoint.dev.sh"]

# run entrypoint script
ENTRYPOINT ["/usr/src/app/entrypoint.dev.sh"]
