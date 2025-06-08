# Dockerfile for docker
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

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
