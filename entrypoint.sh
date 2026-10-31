#!/bin/bash

set -o errexit  # Abort on nonzero exitstatus
set -o nounset  # Abort on unbound variable
set -o pipefail # Do not hide errors within pipes

python manage.py collectstatic --noinput
python manage.py migrate --noinput

args=()

if [[ -n "${DJANGO_SOCKET:-}" ]]; then
  [[ ! -S "$DJANGO_SOCKET" ]] || rm "$DJANGO_SOCKET"
  args+=(-u "$DJANGO_SOCKET")
else
  args+=(-b 0.0.0.0 -p 8000)
fi

exec daphne jelkob.asgi:application "${args[@]}"
