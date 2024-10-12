ifndef APP_PORT
override APP_PORT = 8000
endif

ifndef APP_HOST
override APP_HOST = 0.0.0.0
endif

args := $(wordlist 2, 100, $(MAKECMDGOALS))
ifndef args
MESSAGE = "No such command (or you pass two or many targets to ). List of possible commands: make help"
else
MESSAGE = "Done"
endif

APPLICATION_NAME = app
CODE = $(APPLICATION_NAME) tests
COUNT_WORKERS = 4  # You should set 2 * count_cores + 1

HELP_FUN = \
	%help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
	if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
    print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
    @{$$help{$$_}},"\n" for keys %help; \

# Commands
help: ##@Help Show this help
	@echo -e "Usage: make [target] ...\n"
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

lint:  ##@Code Check code with pylint
	python3 -m pylint $(CODE)

format:  ##@Code Reformat code with isort and black
	python3 -m isort $(CODE)

run:  ##@Application Run application server
	make migrate head && uvicorn $(APPLICATION_NAME).__main__:app --host ${APP_HOST} --port ${APP_PORT} --reload

run-prod:  ##@Application Run application server
	make migrate head && gunicorn $(APPLICATION_NAME).__main__:app -c ./app/config/gunicorn.py

migrate:  ##@Database Do all migrations in database
	cd $(APPLICATION_NAME)/db && alembic upgrade $(args)

revision:  ##@Database Create new revision file automatically with prefix (ex. 2023_01_01_14cs34f_message.py)
	cd $(APPLICATION_NAME)/db && alembic revision --autogenerate

%::
	echo $(MESSAGE)
