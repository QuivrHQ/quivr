

dev:
	docker compose -f docker-compose.dev.yml up --build

prod:
	docker compose build backend-core
	docker compose -f docker-compose.yml up --build

test-type:
	@if command -v python3 &>/dev/null; then \
		python3 -m pyright; \
	else \
		python -m pyright; \
	fi
