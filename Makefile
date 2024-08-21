.DEFAULT_TARGET=help

## help: Display list of commands
.PHONY: help
help:
	@echo "Available commands:"
	@sed -n 's|^##||p' $(MAKEFILE_LIST) | column -t -s ':' | sed -e 's|^| |'


## dev: Start development environment
.PHONY: dev
dev:
	DOCKER_BUILDKIT=1 docker compose -f docker-compose.dev.yml up --build

dev-build:
	DOCKER_BUILDKIT=1 docker compose -f docker-compose.dev.yml build --no-cache
	DOCKER_BUILDKIT=1 docker compose -f docker-compose.dev.yml up

## prod: Build and start production environment
.PHONY: prod
prod:
	docker compose -f docker-compose.yml up --build

## front: Build and start frontend
.PHONY: front
front:
	cd frontend  && yarn && yarn build && yarn start

## test: Run tests
.PHONY: test
test:
	# Ensure dependencies are installed with dev and test extras
	# poetry install --with dev,test && brew install tesseract pandoc libmagic
	./.run_tests.sh
