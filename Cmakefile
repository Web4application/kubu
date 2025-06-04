.PHONY: all clean run help python cpp ruby

all: python cpp ruby

clean:
	$(MAKE) -C python clean
	$(MAKE) -C cpp clean
	$(MAKE) -C ruby clean

run:
	$(MAKE) -C python run
	$(MAKE) -C cpp run
	$(MAKE) -C ruby run

python:
	$(MAKE) -C python

cpp:
	$(MAKE) -C cpp

ruby:
	$(MAKE) -C ruby

help:
	@echo "Top-Level Makefile:"
	@echo "  make all     - Build all modules"
	@echo "  make run     - Run all modules"
	@echo "  make clean   - Clean all modules"
	@echo "  make python  - Python tasks"
	@echo "  make cpp     - C++ tasks"
	@echo "  make ruby    - Ruby tasks"
