# Use official Python runtime as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY app.py /app/

# Install Flask and Gunicorn
RUN pip install flask gunicorn

# Expose port 5000
EXPOSE 5000

# Run the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]