#!/bin/sh
set -e

if [ "$ENTRY_POINT" = "run_server" ]; then
  gunicorn --bind 0.0.0.0:8000 private_library.wsgi
elif [ "$ENTRY_POINT" = "migrate_and_collectstatic" ]; then
  python manage.py migrate --noinput
  python manage.py collectstatic --noinput
elif [ "$ENTRY_POINT" = "dump_db" ]; then
  filename="library_data_$(date +%d)_$(date +%m)_$(date +%y).json"
  python manage.py dumpdata > "/dumps/$filename"
fi

exec "$@"