# Taiga docker setup

## About

This is example Docker Compose file for running [Taiga](https://taiga.io) project management platform for agile developers, designers and project managers with taiga-events and ssl-enabled reverse proxy with all images based on alpine:latest.

## Basic usage

1) Clone this repository.
`git clone --depth=1 -b master https://github.com/docker-taiga/taiga.git`
1) Adjust `TAIGA_HOST`, `TAIGA_SECRET`, `POSTGRES_PASSWORD` and `RABBIT_PASSWORD` in `variables.env` file.
1) (Optional) If you want to enable SSL, change `TAIGA_SCHEME` and `TAIGA_PORT` variables accordingly, create `cert` folder and put ssl certificate and key inside. Default certificate and key filenames are `fullchain.pem` and `privkey.pem`. This can be changed by adding `CERT_NAME` and `CERT_KEY` environment variables to the service `proxy`. Alternatively, if you use certbot to acquire certificates, point volume `/taiga-cert` of the `proxy` service to the location of certificates, e.g. `/etc/letsencrypt/live/yourdomain.com`.
1) `docker-compose --env-file variables.env up`

The default username and password taiga creates is `admin` with password `123123`.

## Upgrading from Taiga v5 to v6

**IMPORTANT:** Please read and follow the steps outlined in the [official document](https://taigaio.github.io/taiga-doc/dist/upgrades-5to6.html) in order to migrate data and port configuration to the new version.

## Individual images

- **Taiga backend**
[`docker pull dockertaiga/back`](https://hub.docker.com/r/dockertaiga/back/)
- **Taiga frontend**
[`docker pull dockertaiga/front`](https://hub.docker.com/r/dockertaiga/front/)
- **RabbitMQ server**
[`docker pull dockertaiga/rabbit`](https://hub.docker.com/r/dockertaiga/rabbit/)
- **Taiga events**
[`docker pull dockertaiga/events`](https://hub.docker.com/r/dockertaiga/events/)
- **Nginx reverse proxy**
[`docker pull dockertaiga/proxy`](https://hub.docker.com/r/dockertaiga/proxy/)

## Environment variables

- `TAIGA_HOST` - Taiga hostname to use with this taiga setup.
- `TAIGA_SCHEME` - Taiga URL scheme (http/https). Default is 'http'.
- `TAIGA_PORT` - Taiga port to use. Default is 80.
- `TAIGA_BACK_HOST` - Backend hostname. Default is `back` service.
- `TAIGA_FRONT_HOST` - Frontend hostname. Default is `front` service.
- `EVENTS_HOST` - Events hostname. Default is `events` service.
- `TAIGA_SECRET` - Django secret key.

---

- `ENABLE_SSL` - Enable SSL termination (yes/no). Default is 'no'.
- `CERT_NAME` - Name of certificate file. Default is `fullchain.pem`.
- `CERT_KEY` - Name of certificate key file. Default is `privkey.pem`.

---

- `POSTGRES_HOST` - PostgeSQL hostname. Default is `db` service.
- `POSTGRES_DB` - Database name.
- `POSTGRES_USER` - PostgreSQL username.
- `POSTGRES_PASSWORD` - PostgreSQL password.

---

- `RABBIT_HOST` - RabbitMQ hostname. Default is `rabbit` service.
- `RABBIT_USER` - RabbitMQ username.
- `RABBIT_PASSWORD` - RabbitMQ password.
- `RABBIT_VHOST` - RabbitMQ virtual host name.


## Configuration

By default configuration volume is `./conf` with config files `./conf/back/config.py` for backend, `./conf/front/config.json` for frontend and `./conf/proxy/nginx.conf` for reverse proxy. Generated config files are placed here on first run and can be modified to specify e.g. SMTP server configuration.

## Persistence

Volume `./data` contains postgresql data and taiga media files for persistence and backup purposes.

## Upgrading

Before upgrading be sure to check taiga-back [changelog](https://github.com/taigaio/taiga-back/blob/master/CHANGELOG.md) for any breaking changes
and check for any modified configuration files in this repo to see what configs need to be adjusted accordignly.

1) Update the version in `variables.env` or pull from this repo.
1) `docker-compose --env-file variables.env pull`
1) `docker-compose --env-file variables.env up`
