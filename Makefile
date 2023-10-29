DOCKER_REPOSITORY := kaggle-docker
DOCKERFILE := Dockerfile
DOCKER_COMPOSE := docker-compose.yml

.PHONY: build
build:
	docker build \
		-t $(DOCKER_REPOSITORY) \
		-f $(DOCKERFILE) \
		.

.PHONY: cup
cup:
	docker-compose \
		-f ./$(DOCKER_COMPOSE) \
		up -d

.PHONY: cdown
cdown:
	docker-compose \
		-f ./$(DOCKER_COMPOSE) \
		down -v