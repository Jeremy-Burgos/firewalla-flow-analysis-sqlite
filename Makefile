PYTHON ?= python3
PIP ?= pip
PYTEST ?= pytest

.PHONY: help install run-example test

help:
	@echo "Available targets:"
	@echo "  install      Create local dependency baseline"
	@echo "  run-example  Run the example CSV import"
	@echo "  test         Run tests"

install:
	$(PIP) install --upgrade pip

run-example:
	$(PYTHON) scripts/firewalla_csv_to_sqlite.py \
		--csv examples/sample-firewalla-export.csv \
		--db firewalla_flows.sqlite3 \
		--source-tz UTC \
		--local-cidr 192.168.1.0/24 \
		--local-cidr 10.0.0.0/8 \
		--summary-csv blocked_inbound_ranked.csv

test:
	$(PYTEST)