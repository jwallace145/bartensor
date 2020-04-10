# Bartensor

Bartensor is community-driven, intelligent platform that connects alcohol consumers around the world. This Django web application allows people to easily search for their favorite drink's recipe or discover new similar drinks from our SQLite database and much more. Bartensor allows registered users to create custom drinks and add their recipes to our database and vote on other drink recipes. Bartensor aims to connect communities through alcohol so registered users can friend and comment with other users and their custom created drinks.

## Getting Started

This set of instructions will help you locally install the required python dependencies and run the Bartensor Django server for development purposes.

### Python Application Dependencies

Bartensor uses Django3.0.3 - a python framework - so there are required python dependencies listed in the requirements.txt file of this repository.

    appdirs==1.4.3
    asgiref==3.2.3
    astroid==2.3.3
    atomicwrites==1.3.0
    attrs==19.3.0
    autopep8==1.5
    awsebcli==3.17.1
    bcrypt==3.1.7
    beautifulsoup4==4.8.2
    blessed==1.17.4
    botocore==1.14.17
    bs4==0.0.1
    cached-property==1.5.1
    cachetools==4.0.0
    cement==2.8.2
    certifi==2019.11.28
    cffi==1.14.0
    chardet==3.0.4
    colorama==0.3.9
    coverage==5.0.3
    cryptography==2.9
    distlib==0.3.0
    Django==3.0.3
    django-crispy-forms==1.8.1
    django-jenkins==0.110.0
    docker==4.2.0
    docker-compose==1.25.4
    dockerpty==0.4.1
    docopt==0.6.2
    docutils==0.15.2
    entrypoints==0.3
    filelock==3.0.12
    flake8==3.7.9
    future==0.16.0
    google-api-core==1.16.0
    google-auth==1.11.2
    google-cloud-speech==1.3.2
    googleapis-common-protos==1.51.0
    grpcio==1.27.2
    ibm-cloud-sdk-core==1.5.1
    ibm-watson==4.2.1
    idna==2.7
    isort==4.3.21
    jmespath==0.9.5
    jsonschema==3.2.0
    lazy-object-proxy==1.4.3
    lxml==4.5.0
    mccabe==0.6.1
    more-itertools==8.2.0
    nltk==3.4.5
    packaging==20.1
    paramiko==2.7.1
    pathspec==0.5.9
    pep8==1.7.1
    Pillow==7.0.0
    pluggy==0.13.1
    protobuf==3.11.3
    psycopg2-binary==2.8.4
    py==1.8.1
    pyasn1==0.4.8
    pyasn1-modules==0.2.8
    pycodestyle==2.5.0
    pycparser==2.20
    pyflakes==2.1.1
    PyJWT==1.7.1
    pylint==2.4.4
    pylint-django==2.0.14
    pylint-plugin-utils==0.6
    PyNaCl==1.3.0
    pyparsing==2.4.6
    pyrsistent==0.16.0
    pytest==5.3.5
    pytest-cov==2.8.1
    python-dateutil==2.8.0
    pytz==2019.3
    PyYAML==5.2
    requests==2.20.1
    rsa==4.0
    selenium==3.141.0
    semantic-version==2.5.0
    six==1.11.0
    soupsieve==2.0
    sqlparse==0.3.0
    termcolor==1.1.0
    texttable==1.6.2
    urllib3==1.24.3
    virtualenv==16.7.9
    wcwidth==0.1.8
    websocket-client==0.48.0
    wrapt==1.11.2

### Install Python Application Dependencies

First, clone this repository to your local machine.

    git clone https://github.com/jwallace317/Gin-and-Tensor.git

Next, navigate into the cloned directory and create a python3 virtual environment with virtualenv.

    python3 -m virtualenv <virtual environment name>

Now with the virtual environment activated, install the python dependencies with pip and the requirements.txt file.

    source <virtual environment name>/bin/activate
    pip install -r requirements.txt

### Run Database Migrations

Django creates migrations to record changes in the database design. The migrations must be applied prior to running the server to ensure correct functionality.

To make migrations, run the following command..

    python manage.py makemigrations

To run migrations, run the following command.

    python manage.py migrate

### Run Development Server

After the python dependencies have been installed and the database migrations have been applied, we can run the development server with the following command.

    python manage.py runserver

## Testing

To run tests enter in the following command

    python manage.py test

To run tests with test coverage enabled, enter in the following command

    coverage run manage.py test

To generate the coverage html report, enter in the following command after the tests have been run with coverage

    coverage html

The generated coverage reports are located in the coverage_reports directory. To view the coverage report, open the index.html file with a web browser or html parser

Run development server with `python manage.py runserver`

When new drinks are added run `python manage.py get_images`
Only drinks where their static image folder is nonexistent will be searched for or downloaded.

For any drinks where the image field in discovery is equal to "images/placeholder.jpg":
    The bot will search google for the name of the respective drink and download the first page of results into
    the folder at '.../static/data/drink_images/00000000from_google'
    within a folder named the drink's discovery ID.
    Enter this folder and delete all but the desired image. Remove the \_\_# from the end of that image's name.
    Move the folder into the drink_images folder when done.

All other drinks where an img src address is specified in the discovery result will be directly downloaded into a folder
named their discovery ID and saved within the drink_images folder.

run `python manage.py db-populate` to insert discovery generated ids and drink names

## Project Structure
