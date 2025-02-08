FROM python:3.11-alpine

WORKDIR /app
COPY pyproject.toml /app/
COPY poetry.lock /app/
RUN pip install poetry && poetry install --no-root
COPY ./app /app
EXPOSE 8000
CMD poetry run gunicorn --bind 0.0.0.0:8000 app:app
