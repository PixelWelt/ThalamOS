FROM python:3.14-alpine
COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml /app/

RUN apk add --no-cache build-base libffi-dev openssl-dev cargo curl
RUN pip install --upgrade pip
RUN uv lock

COPY ./app /app
EXPOSE 8000

CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
