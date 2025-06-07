.PHONY: all clean run test lint python cpp ruby

all: python cpp ruby

run: run-python run-cpp run-ruby

clean:
	@echo "Cleaning..."
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -r {} +
	rm -f app
	rm -rf .bundle vendor

# PYTHON
python: install-python

install-python:
	pip install -r requirements.txt

run-python:
	python main.py

# C++
cpp: build-cpp

build-cpp:
	g++ -Wall -std=c++17 -o app main.cpp

run-cpp: build-cpp
	./app

# RUBY
ruby: install-ruby

install-ruby:
	bundle install || true

run-ruby:
	ruby main.rb

# Testing
test:
	pytest tests/test_main.py
	rspec tests/test_main.rb || true

lint:
	flake8 main.py || true
	rubocop main.rb || true

help:
	@echo "Usage:"
	@echo "  make all      - Build all languages"
	@echo "  make run      - Run all programs"
	@echo "  make clean    - Clean all build artifacts"
	@echo "  make test     - Run Python + Ruby tests"
	@echo "  make lint     - Run linters"
