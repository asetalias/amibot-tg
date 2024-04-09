install: ## Install dependencies and pre-commit hooks + setup virtual environment.
	@echo "🚀 Creating virtual environment using pyenv and poetry"
	@poetry install
	@poetry run pre-commit install
	@poetry shell

gen: ## Generate proto buffs.
	rm -f gen/*.py; cd proto; buf generate; cd ...

mongo: ## Run mongodb server in docker.
	docker run -d --name py-mongo -p 27017:27017 mongo

dev: ## Run amibot server
	poetry run nodemon --no-colors --exec python main.py

docker: ## Builds the docker image for amibot server.
	@docker build -t py-amibot .

dockerRun: ## Runs the amibot server in docker.
	@docker run -d --name py-amibot -p 3333:3333 py-amibot

check: ## Run code quality tools.
	@echo "🚀 Checking Poetry lock file consistency with 'pyproject.toml': Running poetry lock --check"
	@poetry check --lock
	@echo "🚀 Linting code: Running pre-commit"
	@poetry run pre-commit run -a

help: ## List available targets with respective description.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: gen, mongo, dev, env, docker, dockerRun, install, check, help
.DEFAULT_GOAL := help
