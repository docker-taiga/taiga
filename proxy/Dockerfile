FROM nginx:alpine

ENV TAIGA_HOST=taiga.lan \
	TAIGA_BACK_HOST=127.0.0.1 \
	TAIGA_FRONT_HOST=127.0.0.1 \
	EVENTS_HOST=127.0.0.1 \
	ENABLE_SSL=no \
	CERT_NAME=fullchain.pem \
	CERT_KEY=privkey.pem

WORKDIR /etc/nginx/conf.d

RUN rm default.conf

COPY nginx.conf nginx_ssl.conf proxy_params /tmp/taiga-conf/
COPY start.sh /

EXPOSE 80 443

VOLUME ["/taiga-cert", "/taiga-conf"]

CMD ["/start.sh"]
