ifeq ($(shell test -e '.env' && echo -n yes),yes)
	include .env
endif

args := $(wordlist 2, 100, $(MAKECMDGOALS))
ifndef args
MESSAGE = "No such command (or you pass two or many targets to ). List of possible commands: make help"
else
MESSAGE = "Done"
endif

APPLICATION_NAME = app
TEST = poetry run python3 -m pytest --verbosity=2 --showlocals --log-level=DEBUG

HELP_FUN = \
	%help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
	if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
    print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
    @{$$help{$$_}},"\n" for keys %help; \

# Commands
env:  ##@Environment Create .env file with variables
	@$(eval SHELL:=/bin/bash)
	@cp .env.sample .env

help: ##@Help Show this help
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

docker-up-build:  ##@Application Run and build application server
	docker-compose -f docker-compose.yml up --build --remove-orphans

docker-up-buildd:  ##@Application Run and build application server in daemon
	docker-compose -f docker-compose.yml up -d --build --remove-orphans

docker-up:  ##@Application Run application server
	docker-compose -f docker-compose.yml up

docker-upd:  ##@Application Run application server in daemon
	docker-compose -f docker-compose.yml up -d

docker-down:  ##@Application Stop application in docker
	docker-compose -f docker-compose.yml down --remove-orphans

docker-downv:  ##@Application Stop application in docker and remove volumes
	docker-compose -f docker-compose.yml down -v --remove-orphans

docker-up-build-prod:  ##@Application Run and build application server in production
	docker-compose -f docker-compose.prod.yml up --build --remove-orphans

docker-up-buildd-prod:  ##@Application Run and build application server in daemon in production
	docker-compose -f docker-compose.prod.yml up -d --build --remove-orphans

docker-up-prod:  ##@Application Run application server in production
	docker-compose -f docker-compose.prod.yml up

docker-upd-prod:  ##@Application Run application server in daemon in production
	docker-compose -f docker-compose.prod.yml up -d

docker-down-prod:  ##@Application Stop application in docker in production
	docker-compose -f docker-compose.prod.yml down --remove-orphans

docker-downv-prod:  ##@Application Stop application in docker and remove volumes in production
	docker-compose -f docker-compose.prod.yml down -v --remove-orphans

docker-run-server:  ##@Application Run command in server container
	docker-compose -f docker-compose.yml run server $(args)

lint:  ##@Code Check code with pylint
	make docker-run-command "make lint"

format:  ##@Code Reformat code with isort and black
	make docker-run-command "make format"

revision:  ##@Database Create new revision file automatically with prefix (ex. 2023_01_01_14cs34f_message.py)
	make docker-run-server "bash -c 'cd $(APPLICATION_NAME)/db && alembic revision --autogenerate'"

open-db:  ##@Database Open database inside docker-image
	docker exec -it postgres psql -d $(POSTGRES_DB) -U $(POSTGRES_USER) -p $(POSTGRES_PORT)

open-server:  ##@Application Open container inside docker-image
	make docker-run-server "bash"

docker-clean:  ##@Application Remove all docker objects
	docker system prune --all -f

docker-cleanv:  ##@Application Remove all docker objects with volumes
	docker system prune --all --volumes -f

docker-stop:  ##@Application Stop all docker containers
	@docker rm -f $$(docker ps -aq) || true

%::
	echo $(MESSAGE)
