#!/bin/bash

set -o errexit  # Abort on nonzero exitstatus
set -o nounset  # Abort on unbound variable
set -o pipefail # Do not hide errors within pipes

python manage.py collectstatic --noinput
python manage.py migrate --noinput

exec daphne jelkob.asgi:application -b 0.0.0.0 -p 8000
