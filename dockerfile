FROM python:3.11-slim

WORKDIR /app
COPY /app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-dotenv
COPY . /app
EXPOSE 8000
CMD cd app ; gunicorn --bind 0.0.0.0:8000 app:app
