# pull official base image
FROM ubuntu:18.04

ENV PYTHONUNBUFFERED 1

# update and upgrade apt
RUN apt-get update \
    && apt-get -y upgrade

# set working directory
WORKDIR /usr/src/app

ENV DEBUG 0
ENV SECRET_KEY production
ENV ALLOWED_HOSTS bartensor.biz 18.217.199.76 ec2-18-217-199-76.us-east-2.compute.amazonaws.com
ENV SQL_ENGINE django.db.backends.sqlite3
ENV DATABASE db.sqlite3
ENV BARTENSOR_EMAIL_USERNAME bartensor@gmail.com
ENV BARTENSOR_EMAIL_PASSWORD iupeqdduwlekqjrj
ENV WATSON_DISCOVERY_API_KEY Q48Xgoo6dGAAOSNjdUdho8uwprTEbwgXOBUspsEaTDO2
ENV WATSON_SPEECH_TO_TEXT_API_KEY GUyb9Y0-25JUO7_fZtyLvlDipUAMzROb2vxadUiWJEMX

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
