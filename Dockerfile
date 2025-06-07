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
