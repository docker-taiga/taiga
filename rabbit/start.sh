#!/bin/sh

export RABBITMQ_DEFAULT_VHOST="$RABBIT_VHOST"
export RABBITMQ_DEFAULT_USER="$RABBIT_USER"
export RABBITMQ_DEFAULT_PASS="$RABBIT_PASSWORD"

exec docker-entrypoint.sh rabbitmq-server
