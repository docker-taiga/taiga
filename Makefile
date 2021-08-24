VERSION=6.3.0

TAIGA_BACK_REPO=https://github.com/kaleidos-ventures/taiga-back
TAIGA_FRONT_REPO=https://github.com/kaleidos-ventures/taiga-front-dist
TAIGA_EVENTS_REPO=https://github.com/kaleidos-ventures/taiga-events

default:
	@echo ${VERSION}

build-back:
	docker build -t dockertaiga/back:${VERSION} --build-arg REPO=${TAIGA_BACK_REPO} --build-arg VERSION=${VERSION} back

build-front:
	docker build -t dockertaiga/front:${VERSION} --build-arg REPO=${TAIGA_FRONT_REPO} --build-arg VERSION=${VERSION} front

build-events:
	docker build -t dockertaiga/events:${VERSION} --build-arg REPO=${TAIGA_EVENTS_REPO} --build-arg VERSION=${VERSION} events

build-proxy:
	docker build -t dockertaiga/proxy proxy

build-rabbit:
	docker build -t dockertaiga/rabbit rabbit

build: build-back build-front build-events build-proxy build-rabbit

push-back:
	docker push dockertaiga/back:${VERSION}

push-front:
	docker push dockertaiga/front:${VERSION}

push-events:
	docker push dockertaiga/events:${VERSION}

push-proxy:
	docker push dockertaiga/proxy

push-rabbit:
	docker push dockertaiga/rabbit

push: push-back push-front push-events push-proxy push-rabbit

run:
	docker-compose --env-file variables.env up

cleanup:
	docker-compose --env-file variables.env down -v
	sudo rm -r conf data
