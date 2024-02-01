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

test: .EXPORT_ALL_VARIABLES
	poetry run rasa test e2e e2e_tests

run: .EXPORT_ALL_VARIABLES
	poetry run rasa chat --debug

train: .EXPORT_ALL_VARIABLES
	poetry run rasa train -c config.yml -d domain --data data

train-v3: .EXPORT_ALL_VARIABLES
	cd dm1_versions/version_3 && poetry run rasa train -c config.yml -d domain --data data

actions:
	poetry run rasa run actions

test-passing: .EXPORT_ALL_VARIABLES
	poetry run rasa test e2e e2e_tests/passing

test-failing: .EXPORT_ALL_VARIABLES
	poetry run rasa test e2e e2e_tests/failing

test-one: .EXPORT_ALL_VARIABLES
	poetry run rasa test e2e $(target) --debug

show-results:
	poetry run python scripts/count_lines.py && poetry run python scripts/combine_results.py 

# Versions to test, including the root directory
VERSIONS = root version_1 version_2 version_3 version_4

# Test all versions
test-all: .EXPORT_ALL_VARIABLES
	$(foreach ver,$(VERSIONS),$(MAKE) test-version version=$(ver);)

# Test a specific version (usage: make test-version version=version_3)
test-version: .EXPORT_ALL_VARIABLES
	@mkdir -p test_results
	@if [ "$(version)" = "root" ]; then \
		echo "Testing root directory"; \
		for dir in e2e_tests/*/; do \
		    dirname=$$(basename $$dir); \
		    poetry run rasa test e2e $$dir -m models | grep "failed," > test_results/root_${dirname}.txt; \
		done; \
	else \
		echo "Testing $(version)"; \
		for dir in e2e_tests/*/; do \
		    dirname=$$(basename $$dir); \
		    poetry run rasa test e2e $$dir -m dm1_versions/$(version)/models | grep "failed," > test_results/$(version)_$${dirname}.txt; \
		done; \
	fi

