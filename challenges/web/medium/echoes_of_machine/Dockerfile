FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install flask gunicorn

EXPOSE 5000

CMD ["gunicorn", "--workers", "3", "--threads", "2", "--bind", "0.0.0.0:5000", "app:app"]