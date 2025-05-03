ifneq (,$(wildcard ./.env))
	include .env
	export
	ENV_FILE_PARAM = --env-file .env
endif


ifeq ($(strip $(d)),)
	d := $(shell date +"%d-%m-%Y")
endif

DEV_FILE := docker-compose-dev.yml
DOCKER_COMPOSE_NAME := bunq-yaai-dev

FRONTEND_CON := frontend
BACKEND_CON := backend
DATABASE_CON := postgres

DATABASE_VOLUME := $(DOCKER_COMPOSE_NAME)_db_value
STATIC_VOLUME := $(DOCKER_COMPOSE_NAME)_static_value

#============================

build:
	docker compose -f $(DEV_FILE) up $(c) --build -d --remove-orphans
up:
	docker compose -f $(DEV_FILE) up $(c) -d
down:
	docker compose -f $(DEV_FILE) down $(c)
stop:
	docker compose -f $(DEV_FILE) stop $(c)
restart:
	docker compose -f $(DEV_FILE) stop $(c)
	docker compose -f $(DEV_FILE) up -d $(c)
ps:
	docker compose -f $(DEV_FILE) ps

logs:
	docker compose -f $(DEV_FILE) logs $(c) --follow --tail=100

#=============================

migrate:
	docker compose -f $(DEV_FILE) exec $(FRONTEND_CON) npm run db:migrate

bash:
	docker compose -f $(DEV_FILE) exec $(BACKEND_CON) bash
