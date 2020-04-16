#!/bin/bash

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
chmod 664 /usr/src/app/db.sqlite3
chown www-data /usr/src/app/db.sqlite3
chown www-data /usr/src/app
chmod -R 777 /usr/src/app/media
apache2ctl -D FOREGROUND

exec "$@"
