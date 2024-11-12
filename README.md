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

Clone this repository and install dependencies using Poetry.
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
