ifneq (,$(wildcard ./.env.dev))
    include .env.dev
    export
endif

export-taskwarrior-manual:
	task logsequuid.none: and status.not:deleted and status.not:completed export > data/raw/kbn-/taskwarrior.json

export-taskwarrior:
	task status.not:deleted and status.not:completed export > data/raw/kbn-/taskwarrior.json

start-llm-container:
	invoke llm.start-llm-container

build-image:
	docker build . -t ${IMAGE_NAME}

start:
	docker run --name "${CONTAINER_NAME}" --detach --rm "${IMAGE_NAME}"

lint-check:
	docker exec "${CONTAINER_NAME}" pixi run --environment dev lint-check

format-check:
	docker exec "${CONTAINER_NAME}" pixi run --environment dev format-check

types-check:
	docker exec "${CONTAINER_NAME}" pixi run --environment dev types-check

order-imports-check:
	docker exec "${CONTAINER_NAME}" pixi run --environment dev order-imports-check

connect:
	docker run --name ${CONTAINER_NAME} -it ${IMAGE_NAME} --entrypoint /bin/bash

stop:
	docker stop "${CONTAINER_NAME}"

rm-all-containers:
	docker rm $(docker ps --quiet --all)

test:
	pixi run test
