FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir gunicorn flask

COPY app.py .

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "app:app"]