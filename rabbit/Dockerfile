FROM rabbitmq:alpine

ENV RABBIT_USER=taiga \
    RABBIT_PASSWORD=qwerty \
    RABBIT_VHOST=taiga \
    RABBITMQ_ERLANG_COOKIE=taiga

COPY start.sh /start.sh

ENTRYPOINT ["/start.sh"]
