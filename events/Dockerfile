FROM node:12-alpine

ARG REPO
ARG VERSION

ENV RABBIT_HOST=rabbit \
    RABBIT_PORT=5672 \
    RABBIT_VHOST=taiga \
    RABBIT_USER=taiga \
    RABBIT_PASSWORD=password \
    TAIGA_SECRET=secret

WORKDIR /opt

RUN apk add --no-cache --virtual .build-dependencies git perl \
    && git clone --depth=1 -b $VERSION $REPO taiga-events && cd taiga-events \
    && perl -0777 -pe 's/"devDependencies": \{.*?\},//s' -i package.json \
    && apk del .build-dependencies \
    && yarn --production && yarn global add coffeescript \
    && addgroup -S taiga \
    && adduser -S taiga -G taiga \
    && chown -R taiga:taiga /opt/taiga-events

USER taiga

WORKDIR /opt/taiga-events

EXPOSE 8888

COPY dotenv ./.env
COPY start.sh /

CMD ["/start.sh"]
