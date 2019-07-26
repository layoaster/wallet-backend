PROJECT_ROOT:=.

SRC_DIR = wallet_api/
DOC_DIR = docs/
DOC_BUILD_DIR = doc/_build
TESTS_DIR = tests/
BLACK_CONFIG = .black


help:
	@echo "Please use \`make <target>\` where <target> is one of:"
	@echo "  build      Builds app containers"
	@echo "  start      Gets app containers up & running"
	@echo "  stop       Stop and removes app containers"
	@echo "  logs       Fetches active containers logs"
	@echo "  test       Runs the app suite of tests"
	@echo "  migrate    Applies database migrations"
	@echo "  check      Checks code's quality & style [flake8 and black]"
	@echo "  format     Runs 'black' to format code"
	@echo "  clean      remove temporary/cache/unnecesary files"
.PHONY: help

build:
	@docker-compose build
.PHONY: build

start:
	@docker-compose up -d wallet-backend
.PHONY: start

stop:
	@docker-compose down
.PHONY: stop

logs:
	@docker-compose logs --tail=25
.PHONY: logs

test:
	@docker-compose run --rm test
.PHONY: test

migrate:
	@docker-compose run --rm manage db upgrade
.PHONY: migrate

check:
	@flake8 && \
		black --config $(BLACK_CONFIG) --check $(SRC_DIR) --diff && \
		black --config $(BLACK_CONFIG) --check $(TESTS_DIR) --diff
.PHONY: check

format:
	@black --config $(BLACK_CONFIG) $(SRC_DIR) && \
		black --config $(BLACK_CONFIG) $(TESTS_DIR)
.PHONY: format

clean:
	@find -type d -name "__pycache__" -exec rm  -rf {} \;
	@rm -rf .coverage htmlcov
.PHONY: clean
