test:
	pytest backend/tests

dev:
	docker compose -f docker-compose.dev.yml build backend-core
	docker compose -f docker-compose.dev.yml up --build

dev-saas:
	docker compose -f docker-compose-dev-saas-supabase.yml build backend-core
	docker compose -f docker-compose-dev-saas-supabase.yml up --build

dev-saas-back:
	docker compose -f docker-compose-dev-only-back-saas-supabase.yml build backend-core
	docker compose -f docker-compose-dev-only-back-saas-supabase.yml up --build backend-core

prod:
	docker compose build backend-core
	docker compose -f docker-compose.yml up --build

test-type:
	@if command -v python3 &>/dev/null; then \
		python3 -m pyright; \
	else \
		python -m pyright; \
	fi
