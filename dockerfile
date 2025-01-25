FROM python:3.11-alpine

WORKDIR /app
COPY /app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt
COPY ./app /app
EXPOSE 8000
CMD gunicorn --bind 0.0.0.0:8000 app:app
