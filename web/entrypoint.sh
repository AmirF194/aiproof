#!/bin/sh
set -e

if [ "$DJANGO_MIGRATE_ON_START" = "1" ]; then
  echo ">> applying migrations"
  python manage.py migrate --noinput
fi

if [ "$DJANGO_COLLECTSTATIC_ON_START" = "1" ]; then
  echo ">> collecting static files"
  python manage.py collectstatic --noinput
fi

if [ "$DJANGO_LOAD_ROLES_ON_START" = "1" ]; then
  echo ">> loading roles from CSV"
  python manage.py load_roles --wipe || echo "load_roles failed (continuing)"
fi

exec "$@"
