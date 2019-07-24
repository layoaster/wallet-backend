PROJECT_ROOT:=.

SRC_DIR = wallet_api/
DOC_DIR = docs/
DOC_BUILD_DIR = doc/_build
TESTS_DIR = tests/
BLACK_CONFIG = .black


help:
	@echo "Please use \`make <target>\` where <target> is one of:"
	@echo "  check      to check code's quality & style [flake8 and black]."
	@echo "  format     to run black to format code."
	@echo "  clean      remove temporary/cache/unnecesary files."
.PHONY: help

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
