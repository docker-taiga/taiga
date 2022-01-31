FROM alpine:3.15

ARG REPO
ARG VERSION

ENV TAIGA_HOST=taiga.lan \
    TAIGA_PORT=80 \
    TAIGA_SECRET=secret \
    TAIGA_SCHEME=http \
    POSTGRES_HOST=db \
    POSTGRES_DB=taiga \
    POSTGRES_USER=postgres \
    POSTGRES_PASSWORD=password \
    RABBIT_HOST=rabbit \
    RABBIT_PORT=5672 \
    RABBIT_USER=taiga \
    RABBIT_PASSWORD=password \
    RABBIT_VHOST=taiga \
    DJANGO_SETTINGS_MODULE=settings.config

WORKDIR /srv/taiga

RUN apk --no-cache add python3 py3-pip gettext postgresql-dev libxslt-dev libxml2-dev libjpeg-turbo-dev zeromq-dev libffi-dev openblas-dev lapack-dev nginx \
    && apk add --no-cache --virtual .build-dependencies git g++ musl-dev linux-headers python3-dev binutils-doc autoconf flex bison zlib-dev libjpeg-turbo-dev freetype-dev ncurses-dev gdbm-dev rust cargo \
    && mkdir logs \
    && git clone --depth=1 -b $VERSION $REPO back && cd back \
    && python3 -m venv .venv --prompt taiga-back && source .venv/bin/activate \
    && pip3 install --upgrade pip \
    && pip3 install wheel \
    && pip3 install --no-cache-dir -r requirements.txt \
    && pip3 install --no-cache-dir -r requirements-contribs.txt \
    && rm -rf /root/.cache \
    && apk del .build-dependencies \
    && rm requirements.txt requirements-contribs.txt \
    && find . -name '__pycache__' -exec rm -r '{}' + \
    && find . -name '*pyc' -exec rm -r '{}' + \
    && find . -name '*po' -exec rm -r '{}' + \
    && rm /srv/taiga/back/settings/config.py.dev.example \
    && rm /srv/taiga/back/settings/config.py.prod.example \
    && rm /etc/nginx/http.d/default.conf

WORKDIR /srv/taiga/back

RUN apk --no-cache add su-exec \
    && addgroup -S taiga \
    && adduser -S taiga -G taiga

EXPOSE 80

COPY config.py /tmp/taiga-conf/
COPY nginx.conf /etc/nginx/http.d/
COPY waitfordb.py /
COPY start.sh /

VOLUME ["/taiga-conf", "/taiga-media"]

CMD ["/start.sh"]
