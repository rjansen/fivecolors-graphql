POSTGRES_VERSION        ?= 11.4-alpine
POSTGRES_USER           ?= postgres
POSTGRES_PASSWORD       ?=
POSTGRES_HOST           ?= localhost
POSTGRES_PORT           ?= 5432
POSTGRES_DATABASE       ?= postgres

.PHONY: postgres.run
postgres.run:
	@echo "postgres.run"
	docker run --rm -d --name postgres-run -p $(POSTGRES_PORT):$(POSTGRES_PORT) postgres:$(POSTGRES_VERSION)
	@sleep 7 #wait until database is ready

.PHONY: postgres.kill
postgres.kill:
	@echo "postgres.kill"
	docker kill postgres-run

.PHONY: postgres.scripts
postgres.scripts:
	@echo "postgres.scripts"
	sleep 5
	cat $(POSTGRES_SCRIPTS_DIR)/* | \
		psql -h $(POSTGRES_HOST) -U $(POSTGRES_USER) -d $(POSTGRES_DATABASE) -1 -f -

.PHONY: postgres.psql
postgres.psql:
	@echo "postgres.psql"
	docker run --rm -it --name psql-run postgres:$(POSTGRES_VERSION) \
		psql -h $(POSTGRES_HOST) -U $(POSTGRES_USER) -d $(POSTGRES_DATABASE)

.PHONY: postgres.migrations.run
postgres.migrations.run: postgres.run postgres.migrations

postgres.makemigrations:
	python manage.py makemigrations

postgres.migrate:
	python manage.py migrate

run: postgres.migrate
	python manage.py runserver

dev.dotenv:
	cp contrib/env-sample .env
