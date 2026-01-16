.PHONY: help

help:
	@echo "Usage:"
	@echo "  make all                Setup & Run"
	@echo "  make build              Build the package wheel"
	@echo "  make docker             Build & Run the container"
	@echo "  make pytest             CI: Run test and calculate coverage"
	@echo "  make setup              Create the venv and install dependencies"
	@echo "  make sync               UV: Sync all dependencies"

all:
	$(MAKE) setup
	$(MAKE) sync
	$(MAKE) pytest
	$(MAKE) build
	$(MAKE) docker-build
	$(MAKE) run

docker:
	$(MAKE) docker-clean
	$(MAKE) docker-build
	$(MAKE) docker-run

build:
	uv build

docker-build:
	docker build --file Dockerfile --no-cache --tag ibc .

docker-clean:
	docker stop ibc && docker rm ibc

docker-run:
	docker run --detach --publish 8000:8000 --name ibc ibc

pytest:
	uv run pytest

setup:
	uv venv .venv --python 3.10 --clear

sync:
	uv sync --all-extras --all-packages
