#!/bin/bash

# ensure python version == 3.8
PYTHON_VERSION="$(python --version)"
echo $PYTHON_VERSION

# ensure pip is up to date
PIP_VERSION="$(pip --version)"
echo $PIP_VERSION

if ["$(PYTHON_VERSION)"="Python 3.8.0"]
then
  echo "python version up to date"
fi

# see if virtual env is activate
