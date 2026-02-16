FROM python:3.14-alpine
COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

RUN apk add --no-cache libffi-dev openssl-dev libgcc libstdc++

WORKDIR /app
COPY pyproject.toml uv.lock /app/

RUN pip install --upgrade pip
RUN uv sync --frozen --no-dev

COPY ./app /app
EXPOSE 8000

CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
