VENV = .venv
PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python

.PHONY: all venv install run clean

all: venv install

venv:
	python3 -m venv $(VENV)

install:
	$(PIP) install -U pip
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) -m kubu_hai

clean:
	rm -rf $(VENV) __pycache__ .pytest_cache
