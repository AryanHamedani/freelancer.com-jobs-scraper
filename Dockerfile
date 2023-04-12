# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        libxml2-dev \
        libxslt1-dev \
        python3-dev \
        build-essential \
        redis-server \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Define environment variables
ENV MONGO_URI=mongodb://mongo:27017
ENV MONGO_DATABASE=freelancer_scraper
ENV CELERY_BROKER_URL=redis://redis:6379
ENV CELERY_RESULT_BACKEND=redis://redis:6379
