#
# Synse Server
#

PKG_NAME    := $(shell python setup.py --name)
PKG_VERSION := $(shell python setup.py --version)
IMAGE_NAME  := vaporio/synse-server

GIT_COMMIT  ?= $(shell git rev-parse --short HEAD 2> /dev/null || true)
BUILD_DATE  := $(shell date -u +%Y-%m-%dT%T 2> /dev/null)

.PHONY: clean cover deps docker fmt github-tag lint test version help
.DEFAULT_GOAL := help


clean:  ## Clean up build and test artifacts
	rm -rf build/ dist/ *.egg-info htmlcov/ .coverage* .pytest_cache/ \
		synse_server/__pycache__ tests/__pycache__

cover: test  ## Run unit tests and open the resulting HTML coverage report
	open ./htmlcov/index.html

deps:  ## Update the frozen pip dependencies (requirements.txt)
	tox -e deps

docker:  ## Build the docker image
	docker build \
		--label build_date=${BUILD_DATE} \
		--label version=${PKG_VERSION} \
		--label commit=${GIT_COMMIT} \
		-t ${IMAGE_NAME}:latest .

fmt:  ## Automatic source code formatting (isort, autopep8)
	tox -e fmt

github-tag:  ## Create and push a tag with the current version
	git tag -a v${PKG_VERSION} -m "${PKG_NAME} version v${PKG_VERSION}"
	git push -u origin v${PKG_VERSION}

lint:  ## Run linting checks on the project source code (isort, flake8, twine)
	tox -e lint

test:  ## Run the unit tests
	tox tests/unit

version:  ## Print the version of Synse Server
	@echo "${PKG_VERSION}"

help:  ## Print Make usage information
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort
