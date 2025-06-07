# Use Ubuntu base
FROM ubuntu:22.04

# Set non-interactive mode for apt
ENV DEBIAN_FRONTEND=noninteractive

# Install build tools, Python, Ruby
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    ruby-full \
    build-essential \
    g++ \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ruby bundler
RUN gem install bundler

# Create working dir
WORKDIR /app

# Copy files
COPY . .

# Install Python deps
RUN pip3 install -r requirements.txt

# Install Ruby deps (if Gemfile exists)
RUN bundle install || true

# Build C++ (optional)
RUN g++ -Wall -std=c++17 -o app main.cpp || true

# Entry point prints help
CMD ["make", "help"]

# Base Python stage
FROM python:3.11-slim as python-build
WORKDIR /app/python
COPY python/requirements.txt .
RUN pip install -r requirements.txt
COPY python/ .

# Base C++ stage
FROM gcc:12 as cpp-build
WORKDIR /app/cpp
COPY cpp/ .
RUN make

# Base Ruby stage
FROM ruby:3.2 as ruby-build
WORKDIR /app/ruby
COPY ruby/ .
RUN bundle install

# Final image combining all
FROM debian:bookworm-slim
WORKDIR /app

COPY --from=python-build /app/python /app/python
COPY --from=cpp-build /app/cpp/bin /app/cpp/bin
COPY --from=ruby-build /app/ruby /app/ruby

CMD ["bash"]
