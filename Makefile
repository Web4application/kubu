# Makefile for kubu-hai Python AI CLI tool

APP_NAME = kubu-hai
VENV_DIR = .venv

PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

.PHONY: all venv install run clean install-system uninstall-system

# Default target: create venv and install requirements
all: venv install

# Create Python virtual environment
venv:
	python3 -m venv $(VENV_DIR)

# Install Python dependencies
install:
	$(PIP) install -U pip
	$(PIP) install -r requirements.txt

# Run the application
run:
	$(PYTHON) -m $(APP_NAME)

# Clean virtual environment and pycache
clean:
	rm -rf $(VENV_DIR) __pycache__ .pytest_cache *.pyc

# Optional system-wide install
install-system:
	sudo cp -r $(APP_NAME) /usr/local/lib/$(APP_NAME)
	sudo cp bin/kubu-hai /usr/local/bin/kubu-hai
	sudo chmod +x /usr/local/bin/kubu-hai

# Optional uninstall
uninstall-system:
	sudo rm -rf /usr/local/lib/$(APP_NAME)
	sudo rm -f /usr/local/bin/kubu-hai


# Compiler and flags for C++
CXX = g++
CXXFLAGS = -Wall -std=c++11

# Directories
SRC_DIR = src
BUILD_DIR = build
BIN_DIR = bin
UTILS_DIR = utils

# Source files and object files for C++
SRCS = $(wildcard $(SRC_DIR)/*.cpp)
OBJS = $(patsubst $(SRC_DIR)/%.cpp, $(BUILD_DIR)/%.o, $(SRCS))

# Target executable for C++
TARGET = $(BIN_DIR)/kubu_hai

# Default target
all: $(TARGET)

# Build target for C++
$(TARGET): $(OBJS)
    @mkdir -p $(BIN_DIR)
    $(CXX) $(CXXFLAGS) -o $@ $^

# Compile source files for C++
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
    @mkdir -p $(BUILD_DIR)
    $(CXX) $(CXXFLAGS) -c -o $@ $<

# Clean target
clean:
    rm -rf $(BUILD_DIR) $(BIN_DIR)

# Run target for C++
run: $(TARGET)
    ./$(TARGET)

# Python targets
.PHONY: run_python clean_python

run_python:
    python3 $(UTILS_DIR)/data_loader.py

clean_python:
    rm -f $(UTILS_DIR)/*.pyc

# Ruby targets
.PHONY: run_ruby clean_ruby

run_ruby:
    ruby $(UTILS_DIR)/data_loader.rb

clean_ruby:
    rm -f $(UTILS_DIR)/*.rb

# Phony targets
.PHONY: all clean run
