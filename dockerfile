FROM python:3.11-alpine

WORKDIR /app
COPY pyproject.toml /app/
COPY poetry.lock /app/
RUN python -m pip install --upgrade pip
RUN pip install poetry && poetry install --no-root
COPY ./app /app
RUN python -m compileall /app/*
EXPOSE 8000
CMD poetry run gunicorn --bind 0.0.0.0:8000 app:app
