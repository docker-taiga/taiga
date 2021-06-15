#!/bin/sh

TAIGA_SECRET_ESCAPED=$(echo "$TAIGA_SECRET" | sed 's/[&/\]/\\&/g')
RABBIT_PASSWORD_ESCAPED=$(echo "$RABBIT_PASSWORD" | sed 's/[&/\]/\\&/g')

sed -e 's/$RABBIT_USER/'$RABBIT_USER'/' \
	-e 's/$RABBIT_PASSWORD/'$RABBIT_PASSWORD_ESCAPED'/' \
	-e 's/$RABBIT_HOST/'$RABBIT_HOST'/' \
	-e 's/$RABBIT_PORT/'$RABBIT_PORT'/' \
	-e 's/$RABBIT_VHOST/'$RABBIT_VHOST'/' \
	-e 's/$TAIGA_SECRET/'$TAIGA_SECRET_ESCAPED'/' \
	-i .env

exec yarn run start:production > /dev/stdout 2> /dev/stderr &
NODE_PID=$!

trap 'kill -TERM $NODE_PID' SIGTERM

wait $NODE_PID
