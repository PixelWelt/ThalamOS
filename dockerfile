FROM python:3.14-alpine

WORKDIR /app
COPY pyproject.toml /app/

RUN apk add --no-cache build-base libffi-dev openssl-dev cargo
RUN pip install --no-cache-dir uv \
    && uv install --no-root

COPY ./app /app
EXPOSE 8000

CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
