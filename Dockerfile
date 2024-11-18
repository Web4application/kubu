# Base image
FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc

# Install Python libraries
RUN pip install pandas tensorflow numpy
