#!/bin/sh

cd /srv/taiga/back
source .venv/bin/activate

INITIAL_SETUP_LOCK=/taiga-conf/.initial_setup.lock
if [ ! -f $INITIAL_SETUP_LOCK ]; then
    touch $INITIAL_SETUP_LOCK

    if [ "$TAIGA_SCHEME" == 'http' -a "$TAIGA_PORT" != '80' ] || [ "$TAIGA_SCHEME" == 'https' -a "$TAIGA_PORT" != '443' ]; then
		TAIGA_PORT=":$TAIGA_PORT"
	else
		TAIGA_PORT=''
	fi

	TAIGA_SECRET_ESCAPED=$(echo "$TAIGA_SECRET" | sed 's/[&/\]/\\&/g')
	POSTGRES_PASSWORD_ESCAPED=$(echo "$POSTGRES_PASSWORD" | sed 's/[&/\]/\\&/g')
	RABBIT_PASSWORD_ESCAPED=$(echo "$RABBIT_PASSWORD" | sed 's/[&/\]/\\&/g')

    sed -e 's/$TAIGA_HOST/'$TAIGA_HOST'/' \
        -e 's/$TAIGA_PORT/'$TAIGA_PORT'/' \
        -e 's/$TAIGA_SECRET/'$TAIGA_SECRET_ESCAPED'/' \
        -e 's/$TAIGA_SCHEME/'$TAIGA_SCHEME'/' \
        -e 's/$POSTGRES_HOST/'$POSTGRES_HOST'/' \
        -e 's/$POSTGRES_DB/'$POSTGRES_DB'/' \
        -e 's/$POSTGRES_USER/'$POSTGRES_USER'/' \
        -e 's/$POSTGRES_PASSWORD/'$POSTGRES_PASSWORD_ESCAPED'/' \
        -e 's/$RABBIT_HOST/'$RABBIT_HOST'/' \
        -e 's/$RABBIT_PORT/'$RABBIT_PORT'/' \
        -e 's/$RABBIT_USER/'$RABBIT_USER'/' \
        -e 's/$RABBIT_PASSWORD/'$RABBIT_PASSWORD_ESCAPED'/' \
        -e 's/$RABBIT_VHOST/'$RABBIT_VHOST'/' \
        -i /tmp/taiga-conf/config.py
    cp /tmp/taiga-conf/config.py /taiga-conf/
    ln -sf /taiga-conf/config.py /srv/taiga/back/settings/config.py

    ln -sf /taiga-media /srv/taiga/back/media

    echo 'Waiting for database to become ready...'
    python3 /waitfordb.py
    echo 'Running initial setup...'
    python3 manage.py migrate --noinput
    python3 manage.py loaddata initial_user
    python3 manage.py loaddata initial_project_templates
    python3 manage.py compilemessages
    python3 manage.py collectstatic --noinput
else
    ln -sf /taiga-conf/config.py /srv/taiga/back/settings/config.py
    ln -sf /taiga-media /srv/taiga/back/media

    echo 'Waiting for database to become ready...'
    python3 /waitfordb.py
    echo 'Running database update...'
    python3 manage.py migrate --noinput
    python3 manage.py compilemessages
    python3 manage.py collectstatic --noinput

    echo 'Installing cron jobs...'
    echo '*/5 * * * * cd /srv/taiga/back && /usr/bin/python3 manage.py send_notifications >> /var/log/cron 2>&1' > /etc/crontabs/root
fi

chown -R taiga:taiga /srv/taiga /taiga-conf /taiga-media

su-exec taiga .venv/bin/celery -A taiga worker --concurrency 4 -l INFO &
CELERY_PID=$!

su-exec taiga .venv/bin/gunicorn --workers 4 --timeout 60 -b 127.0.0.1:8000 taiga.wsgi > /dev/stdout 2> /dev/stderr &
TAIGA_PID=$!

mkdir /run/nginx
nginx -g 'daemon off;' &
NGINX_PID=$!

crond >> /var/log/crond 2>&1

trap 'kill -TERM $NGINX_PID; kill -TERM $TAIGA_PID; kill -TERM $CELERY_PID' SIGTERM

wait $NGINX_PID $TAIGA_PID $CELERY_PID
