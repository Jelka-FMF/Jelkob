FROM python:slim AS python

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV POETRY_HOME=/opt/poetry
ENV VENV_HOME=/usr/src/app/.venv
ENV PATH="$POETRY_HOME/bin:$VENV_HOME/bin:$PATH"

WORKDIR /usr/src/app

# Install and setup Poetry
FROM python AS poetry

ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1

RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -

COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev --extras mysql

# Prepare and run app
FROM python AS runtime

EXPOSE 8000

COPY --from=poetry $VENV_HOME $VENV_HOME
COPY . .

CMD ["/bin/bash", "/usr/src/app/entrypoint.sh"]