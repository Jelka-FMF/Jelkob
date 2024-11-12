FROM python:3.13-slim AS python

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV POETRY_HOME=/opt/poetry
ENV VENV_HOME=/usr/src/app/.venv
ENV PATH="$POETRY_HOME/bin:$VENV_HOME/bin:$PATH"

WORKDIR /usr/src/app

FROM python AS poetry

ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1

# Install Poetry
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -

# Install build dependencies
RUN apt-get -y update && apt-get install -y default-libmysqlclient-dev build-essential pkg-config && rm -rf /var/lib/apt/lists/*

# Install app dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev --extras mysql

FROM python AS runtime

EXPOSE 8000

# Needed to make mysqlclient work
RUN apt-get -y update && apt-get install -y libmariadb3 && rm -rf /var/lib/apt/lists/*

# Copy the dependencies and the app to the container
COPY --from=poetry $VENV_HOME $VENV_HOME
COPY . .

# Run the app entrypoint
CMD ["/bin/bash", "/usr/src/app/entrypoint.sh"]
