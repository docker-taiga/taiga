FROM nginx:alpine

ARG REPO
ARG VERSION

ENV TAIGA_HOST=taiga.lan \
    TAIGA_PORT=80 \
    TAIGA_SCHEME=http

WORKDIR /srv/taiga

RUN apk add --no-cache curl \
    && rm /etc/nginx/conf.d/default.conf \
    && mkdir /run/nginx \
    && curl -#L $REPO/archive/$VERSION.tar.gz > dist.tar.gz \
    && tar -xzf dist.tar.gz && mv taiga-front-dist-* front \
    && cd front \
    && rm dist/conf.example.json \
    && addgroup -S taiga \
    && adduser -S taiga -G taiga \
    && chown -R taiga:taiga /srv/taiga/front

WORKDIR /srv/taiga/front/dist

COPY start.sh /
COPY nginx.conf /etc/nginx/conf.d/
COPY config.json /tmp/taiga-conf/

VOLUME ["/taiga-conf"]

CMD ["/start.sh"]
