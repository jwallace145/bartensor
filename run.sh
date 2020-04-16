#!/bin/bash

# set run script variables
DJANGO_PORT=8000
VENV_NAME="env"

# determine os type
if [[ "$OSTYPE" == "darwin"* ]];
then
  # mac osx
  echo "mac osx detected..."

  # export environment variables
  echo "exporting important environment variables..."
  export DEBUG=1
  export SECRET_KEY=local
  export ALLOWED_HOSTS=localhost
  export BARTENSOR_EMAIL_USERNAME=bartensor@gmail.com
  export BARTENSOR_EMAIL_PASSWORD=iupeqdduwlekqjrj
  export WATSON_DISCOVERY_API_KEY=Q48Xgoo6dGAAOSNjdUdho8uwprTEbwgXOBUspsEaTDO2
  export WATSON_SPEECH_TO_TEXT_API_KEY=GUyb9Y0-25JUO7_fZtyLvlDipUAMzROb2vxadUiWJEMX

  # echo environment variables
  echo "important environment variables listed below..."
  echo "DEBUG = $DEBUG"
  echo "SECRET_KEY = $SECRET_KEY"
  echo "ALLOWED_HOSTS = $ALLOWED_HOSTS"
  echo "BARTENSOR_EMAIL_USERNAME = $BARTENSOR_EMAIL_USERNAME"
  echo "BARTENSOR_EMAIL_PASSWORD = $BARTENSOR_EMAIL_PASSWORD"
  echo "WATSON_DISCOVERY_API_KEY = $WATSON_DISCOVERY_API_KEY"
  echo "WATSON_SPEECH_TO_TEXT_API_KEY = $WATSON_SPEECH_TO_TEXT_API_KEY"

  # if virtual environment is not active, activate it
  if [[ "$VIRTUAL_ENV" == "" ]]
  then
    echo "virtual environment not detected..."

    echo "activating virtual environment..."
    pip install virtualenv
    python3 -m virtualenv $VENV_NAME
    source $VENV_NAME/bin/activate

    echo "virtual environment $VENV_NAME activated..."

    if [[ "$VIRTUAL_ENV" == "" ]]
    then
      echo "error during virtual environment initialization..."
      echo "ensure that virtualenv is installed for Python3.8..."
      echo "exiting bash script now..."

      exit 1
    fi
  fi

  # ensure user is in a virtual env
  if [[ "$VIRTUAL_ENV" != "" ]]
  then
    echo "virtual environment detected..."

    # ensure python version starts with 3.8
    PYTHON_VERSION="$(python --version)"
    echo "current python version -> $PYTHON_VERSION"

    if [[ "$PYTHON_VERSION" == "Python 3.8"* ]]
    then
      echo "current python version is up to date -> $PYTHON_VERSION"

      PIP_VERSION="$(pip --version)"
      echo "current pip version -> $PIP_VERSION"
      python -m pip install --upgrade pip

      PIP_VERSION="$(pip --version)"
      echo "upgraded pip version -> $PIP_VERSION"

      echo "install the required dependencies..."
      pip install -r requirements.txt
      echo "pip has installed all required dependencies..."

      echo "django make migrations..."
      python manage.py makemigrations

      echo "django migrate..."
      python manage.py migrate

      echo "starting server at localhost port $DJANGO_PORT"
      python manage.py runserver $DJANGO_PORT
    else
      echo "python version not up to date..."
      echo "current python version -> $PYTHON_VERSION"
      echo "update python version to execute this script..."
      echo "exiting bash script now..."

      exit 1
    fi
  fi
elif [[ "$OSTYPE" == "msys" ]];
then
  # lightweight shell and gnu utilities compiled for windows (part of mingw)
  echo "msys ostype detected..."

  # export environment variables
  echo "exporting important environment variables..."
  setx DEBUG '1'
  setx SECRET_KEY 'local'
  setx ALLOWED_HOSTS 'localhost'
  setx BARTENSOR_EMAIL_USERNAME 'bartensor@gmail.com'
  setx BARTENSOR_EMAIL_PASSWORD 'iupeqdduwlekqjrj'
  setx WATSON_DISCOVERY_API_KEY 'Q48Xgoo6dGAAOSNjdUdho8uwprTEbwgXOBUspsEaTDO2'
  setx WATSON_SPEECH_TO_TEXT_API_KEY 'GUyb9Y0-25JUO7_fZtyLvlDipUAMzROb2vxadUiWJEMX'

  echo "install the required dependencies..."
  pip install -r requirements.txt
  echo "pip has installed all required dependencies..."

  echo "django make migrations..."
  python manage.py makemigrations

  echo "django migrate..."
  python manage.py migrate

  echo "starting server at localhost port $DJANGO_PORT"
  python manage.py runserver $DJANGO_PORT
fi