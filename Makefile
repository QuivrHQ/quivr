#
# virtual environment
#
venv:
	@if [ ! -d "backend/myenv" ]; then \
        echo "Creating virtual environment..."; \
        python3.11 -m venv myenv; \
    else \
      echo "The venv already exist ..."; \
    fi

activate:
	echo "Activating virtual environment ..."; \
  	. backend/myenv/bin/activate;

install:
	@echo "Installing dependencies ..."; \
	cd backend; \
	pip install --upgrade pip; \
    pip install -r requirements.txt;


# Target to create and set up the environment
setup: venv activate install

.PHONY: venv activate install setup


#
# docker compose
#

dev:
	docker compose -f docker-compose.dev.yml up --build

prod:
	docker compose -f docker-compose.yml up --build

test-type:
	@if command -v python3 &>/dev/null; then \
		python3 -m pyright; \
	else \
		python -m pyright; \
	fi
