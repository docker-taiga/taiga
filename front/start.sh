#!/bin/sh

INITIAL_SETUP_LOCK=/taiga-conf/.initial_setup.lock
if [ ! -f $INITIAL_SETUP_LOCK ]; then
  touch $INITIAL_SETUP_LOCK

  [ "$TAIGA_SCHEME" == 'https' ] && TAIGA_WS_SCHEME=wss || TAIGA_WS_SCHEME=ws

  if [ "$TAIGA_SCHEME" == 'http' -a "$TAIGA_PORT" != '80' ] || [ "$TAIGA_SCHEME" == 'https' -a "$TAIGA_PORT" != '443' ]; then
    TAIGA_PORT=":$TAIGA_PORT"
  else
    TAIGA_PORT=''
  fi

  sed -e 's/$TAIGA_HOST/'$TAIGA_HOST'/' \
      -e 's/$TAIGA_PORT/'$TAIGA_PORT'/' \
      -e 's/$TAIGA_SCHEME/'$TAIGA_SCHEME'/' \
      -e 's/$TAIGA_WS_SCHEME/'$TAIGA_WS_SCHEME'/' \
      -i /tmp/taiga-conf/config.json
  cp /tmp/taiga-conf/config.json /taiga-conf/
  ln -sf /taiga-conf/config.json /srv/taiga/front/dist/conf.json
else
    ln -sf /taiga-conf/config.json /srv/taiga/front/dist/conf.json
fi

chown -R taiga:taiga /srv/taiga/front /taiga-conf

exec nginx -g 'daemon off;'
