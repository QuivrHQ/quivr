test:
	pytest backend/

dev-build:
	DOCKER_BUILDKIT=1 docker compose -f docker-compose.dev.yml build backend-core
	DOCKER_BUILDKIT=1 docker compose -f docker-compose.dev.yml up --build

dev:
	DOCKER_BUILDKIT=1 docker compose -f docker-compose.dev.yml up


dev-saas:
	docker compose -f docker-compose-dev-saas-supabase.yml build backend-core
	docker compose -f docker-compose-dev-saas-supabase.yml up --build

dev-saas-back:
	docker compose -f docker-compose-dev-only-back-saas-supabase.yml build backend-core
	docker compose -f docker-compose-dev-only-back-saas-supabase.yml up --build backend-core

dev-stan:
	docker compose -f docker-compose-no-frontend.dev.yml up --build 

prod:
	docker compose build backend-core
	docker compose -f docker-compose.yml up --build

test-type:
	@if command -v python3 &>/dev/null; then \
		python3 -m pyright; \
	else \
		python -m pyright; \
	fi

front:
	cd frontend  && yarn build && yarn start

test:
	cd backend/core && ./scripts/run_tests.sh