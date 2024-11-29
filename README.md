# Jelkob

Main website for accessing and managing Jelka FMF.

## About

This repository contains a Django project for managing Jelka FMF patterns and runner.
It serves as a cloud service for [Jelkly](https://github.com/Jelka-FMF/Jelkly) to store
the user-submitted patterns, and a data source for [Korenine](https://github.com/Jelka-FMF/Korenine)
to host all patterns and control the runner state. Additionally, it provides a website
for viewing the patterns and information about the project.

## Installation

### Local

Clone this repository and install dependencies using [Poetry](https://python-poetry.org/).
Use any ASGI server to run `jelkob.asgi:application`.

### Docker

Install container from [the container registry](https://github.com/Jelka-FMF/Jelkob/pkgs/container/jelkob).

You can use a pre-made [`docker-compose.yml`](docker-compose.yml) file to run the container
and all required services. You need to provide a `.env` file with the required environment
variables and set up a reverse proxy to serve the static files.

The Daphne ASGI server is exposed on port 8000.

The static files are stored in `/usr/src/app/static/`. You need to mount this directory
as a volume and configure your web server to serve files from it.

The user-uploaded files are stored in `/usr/src/app/uploads/`. You also need to mount
this directory as a volume. Serving files from this directory is optional, but if you do
that, be sure to understand the security implications of serving untrusted user files.

## Configuration

The project needs to be configured using environment variables.
Check [`settings.py`](jelkob/settings.py) for a list of them.

You can create an initial Django user using:

```shell
python manage.py createsuperuser
```

## Development

Clone this repository and install dependencies using [Poetry](https://python-poetry.org/).

You can configure the project as described above. You will likely want to set the
`DJANGO_DEBUG` environment variable to `1` for development. The default values for most
other settings should work fine, but you might need to configure the URLs of services
when developing and testing parts that require them.

After configuring the project, you can run the development server using:

```shell
python manage.py runserver
```

Generate migrations and apply them using:

```shell
python manage.py makemigrations
python manage.py migrate
```

Generate the translation files using:

```shell
python manage.py makemessages --locale sl --ignore venv
```

After translating the PO files, compile them using:

```shell
python manage.py compilemessages
```

To make localization work, you will need to have the `gettext` command available.
You can read more about it in the [Django documentation](https://docs.djangoproject.com/en/5.1/topics/i18n/translation/#how-to-create-language-files).

Before committing your changes, make sure the code passes the linter and formatter:

```shell
ruff check
ruff format
```

Contribute your changes to the `develop` branch. When the changes are ready to
be deployed to production, we will merge them into the `main` branch.
