FROM python:3.11-slim

WORKDIR /app
COPY /app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
RUN pip install python-dotenv
EXPOSE 80
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
