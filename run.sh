#!/bin/bash

# export environment variables
export BARTENSOR_EMAIL_USERNAME=
export BARTENSOR_EMAIL_PASSWORD=

# set run script variables
DJANGO_PORT=8000
VENV_NAME="env"

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

echo "virtual environment detected..."

# ensure python version == 3.8
PYTHON_VERSION="$(python --version)"
echo "current python version -> $PYTHON_VERSION"

if [[ "$PYTHON_VERSION" == "Python 3.8.0" ]]
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