FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

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

# Use Microsoft's universal dev container as base
FROM mcr.microsoft.com/devcontainers/universal:2

# Metadata
LABEL maintainer="Web4application Team <team@web4application.com>"

# Update & install system dependencies for Python, C++, Ruby, Node
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    python3.11 python3-pip python3-venv python3.11-venv \
    ruby-full \
    nodejs npm \
    git \
    curl \
    docker.io \
    postgresql-client \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

# Install Bundler for Ruby
RUN gem install bundler

# Upgrade npm & install common global node tools (optional)
RUN npm install -g npm@latest yarn

# Set Python3.11 as default python3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Create workspace directory
WORKDIR /workspace

# Copy your requirement files (adjust if you want)
COPY requirements.txt /workspace/
RUN pip3 install --no-cache-dir -r requirements.txt

# (Optional) Copy Ruby gems file and install gems
COPY Gemfile* /workspace/
RUN if [ -f Gemfile ]; then bundle install; fi

# (Optional) Copy package.json and install node modules
COPY package.json package-lock.json* /workspace/
RUN if [ -f package.json ]; then npm install; fi

# Add vscode user permissions to use docker (docker-in-docker)
RUN usermod -aG docker vscode

# Default shell
CMD [ "/bin/bash" ]
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

LABEL org.opencontainers.image.source="https://github.com/Web4application/kubu.git"
CMD ["bash"]
