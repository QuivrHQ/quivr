
dev:
	DOCKER_BUILDKIT=1 docker compose -f docker-compose.dev.yml up --build

prod:
	docker compose build backend-core
	docker compose -f docker-compose.yml up --build


front:
	cd frontend  && yarn build && yarn start

test:
	# Ensure dependencies are installed with dev and test extras
	# poetry install --with dev,test && brew install tesseract pandoc libmagic
	./.run_tests.sh
