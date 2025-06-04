# Kubu-Hai Makefile

APP_NAME = kubu-hai
VENV_DIR = .venv
BIN_PATH = /usr/local/bin/$(APP_NAME)

.PHONY: all build run clean install uninstall

all: build

# Simulates a build step by preparing the Python environment
build:
	python3 -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r requirements.txt

# Runs the app (adjust if not __main__)
run:
	$(VENV_DIR)/bin/python -m $(APP_NAME)

# Removes the build artifacts
clean:
	rm -rf $(VENV_DIR) *.pyc __pycache__

# Installs the script to /usr/local/bin
install:
	sudo cp bin/$(APP_NAME) $(BIN_PATH)
	sudo chmod +x $(BIN_PATH)

# Uninstalls the CLI tool
uninstall:
	sudo rm -f $(BIN_PATH)
