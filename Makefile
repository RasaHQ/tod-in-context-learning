.PHONY: install test run train test-passing test-failing test-all test-version help actions

-include .env

help:
	@echo "install - install dependencies"
	@echo "test - run tests"
	@echo "run - run chatbot"
	@echo "train - train chatbot"

.EXPORT_ALL_VARIABLES:

install:
	poetry install

train-version: .EXPORT_ALL_VARIABLES
	cd version_$(version) && poetry run rasa train -c config.yml -d domain --data data

actions:
	poetry run rasa run actions

show-results:
	poetry run python scripts/count_lines.py && poetry run python scripts/combine_results.py 

# Versions to test, including the root directory
VERSIONS = version_1 version_2 version_3

# Test all versions
test-all: .EXPORT_ALL_VARIABLES
	$(foreach ver,$(VERSIONS),$(MAKE) test-version version=$(ver);)

# Test a specific version (usage: make test-version version=1)
test-version: .EXPORT_ALL_VARIABLES
	@mkdir -p test_results
	@echo "Testing version $(version)"; \
	current_dir=$$(pwd); \
	./run_tests.sh $(version) $$current_dir;

