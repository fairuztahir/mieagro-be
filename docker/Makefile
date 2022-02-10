.PHONY: build up start down destroy stop restart logs logs-api ps dangling-volume clear-dangling-volume dangling-image clear-dangling-image clear-volume clear-image clear-container prune scan
ifeq '$(findstring ;,$(PATH))' ';'
    UNAME := Windows
else
    UNAME := $(shell uname 2>/dev/null || echo Unknown)
    UNAME := $(patsubst CYGWIN%,Cygwin,$(UNAME))
    UNAME := $(patsubst MSYS%,MSYS,$(UNAME))
    UNAME := $(patsubst MINGW%,MSYS,$(UNAME))
endif
ifneq (,$(wildcard ./.env))
    include .env
    export
endif
project_id := $(or ${project_id}, ${PROJECT_ID})
env := $(or ${env}, ${APP_ENV})
ifeq ($(UNAME),Windows)
    OSCMD := set "COMPOSE_DOCKER_CLI_BUILD=1" && set "DOCKER_BUILDKIT=1"
else
    OSCMD := export COMPOSE_DOCKER_CLI_BUILD=1 && export DOCKER_BUILDKIT=1
endif

# Note: Cached files are in /var/lib/docker/overlay2
all:                     ## Default process Build and Up containers with cache
	@echo starting --$(env) build and up containers
	@$(OSCMD) && docker compose -f docker-compose.yml -f docker-compose.$(env).yml up -d --build

.PHONY: test
test:                    ## Default process Build and Up containers with cache for test
	@echo starting --test build and up containers
	@$(OSCMD) && docker compose -f docker-compose.test.yml up -d --build

.PHONY: test-destroy
test-destroy:            ## Remove container service and volumes for test
	@docker compose -f docker-compose.test.yml down -v $(c)

.PHONY: fresh
fresh:                   ## Build and Up containers without cache
	@echo starting --$(env) build and up containers
	@$(OSCMD) && docker compose -f docker-compose.yml -f docker-compose.$(env).yml build --no-cache --progress auto
	@docker compose -f docker-compose.yml -f docker-compose.$(env).yml up -d

.PHONY: help
help:                    ## Show command list
	@echo usage: 
	@echo       make [ target ] [ optional ]
	@echo ``
	@echo optional:
	@echo       env=[ environment ]
	@echo       c=[ command ]
	@echo `` 
	@echo target:
	@echo ``
	@awk '/^[a-zA-Z0-9\-_+. ]*:[a-zA-Z0-9\-_+. ]*#{2}/ { print; }' $(MAKEFILE_LIST)

.PHONY: hupdate
hupdate:
	@$(OSCMD) && docker compose -f docker-compose.yml -f docker-compose.$(env).yml up -d --no-deps --build $(c)
build:                   ## Build container without cache
	@$(OSCMD) && docker compose -f docker-compose.yml -f docker-compose.$(env).yml build --no-cache --progress auto $(c)
up:                      ## Up/Run containers in detach mode
	@docker compose -f docker-compose.yml -f docker-compose.$(env).yml up -d $(c)
start:                   ## Start all containers or specific container with c=<name>
	@docker compose -f docker-compose.yml -f docker-compose.$(env).yml start $(c)
down:                    ## Remove all containers or specific container with c=<name>
	@docker compose -f docker-compose.yml -f docker-compose.$(env).yml down $(c)
destroy:                 ## Remove container service and volumes
	@docker compose -f docker-compose.yml -f docker-compose.$(env).yml down -v $(c)
stop:                    ## Stop all containers or specific container with c=<name>
	@docker compose -f docker-compose.yml -f docker-compose.$(env).yml stop $(c)
restart:                 ## Restart all containers or specific container with c=<name>
	@docker compose -f docker-compose.yml -f docker-compose.$(env).yml stop $(c) && \
    docker compose -f docker-compose.yml -f docker-compose.$(env).yml up -d $(c)
logs:                    ## View all log messages or specific service log with c=<name>
	@docker compose -f docker-compose.yml -f docker-compose.$(env).yml logs --tail=100 -f $(c)
logs-api:                ## Display first 100 log messages for API
	@docker compose -f docker-compose.yml logs --tail=100 -f api
ps:                      ## Overview of all running containers
	@docker compose -f docker-compose.yml -f docker-compose.$(env).yml ps
dangling-volume:         ## List of dangling volumes
	@docker volume ls -f dangling=true
clear-dangling-volume:   ## Remove all dangling volumes
	@docker volume prune
dangling-image:          ## List of dangling images
	@docker images -f dangling=true
clear-dangling-image:    ## Remove all dangling images
	@docker image prune
clear-volume:            ## Remove all volumes
	@docker volume rm $(shell docker volume ls -q)
clear-image:             ## Remove all images
	@docker rmi $(shell docker images -aq)
clear-container:         ## Remove all containers
	@docker container rm $(shell docker ps -aq) -f
prune:					 ## Remove all cached, existing images, containers
	@docker system prune -a
scan:					 ## Scan existing images with Snyk, c=<image-name>
	@docker scan $(project_id)/koavue-$(c)

# Sorry, lazy to install node tool to create a commit message..
# https://dzone.com/articles/using-conventional-commit-in-project
.PHONY: ct
ct:
	@echo "feat: - A new feature"
	@echo "fix: - A bug fix"
	@echo "docs: - Documentation only changes"
	@echo "style: - Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)"
	@echo "refactor: - A code change that neither fixes a bug nor adds a feature"
	@echo "perf: - A code change that improves performance"
	@echo "test: - Adding missing tests or correcting existing tests"
	@echo "build: - Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)"
	@echo "ci: - Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)"
	@echo "chore: - Other changes that don't modify src or test files"
	@echo "revert: - Reverts a previous commit"

.PHONY: g-status
g-status:
	@git status
.PHONY: g-add
g-add: ct
	@git add $(c)
	@git status
.PHONY: del-local-branch
del-local-branch:
	@git branch -d $(c)
.PHONY: del-local-remote
del-remote-branch:
	@git push origin --delete $(c)
