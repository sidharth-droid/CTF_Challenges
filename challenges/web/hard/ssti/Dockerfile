FROM python:3.9-slim
WORKDIR /app
COPY app.py /app/
RUN pip install flask gunicorn
ENV FLAG=FLAG{ssti_tinkerer_win}
EXPOSE 5000
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "app:app"]