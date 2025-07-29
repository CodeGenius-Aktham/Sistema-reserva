FROM python:3.10-buster # Cambiado de slim-buster

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE $PORT
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "wsgi:app"]
