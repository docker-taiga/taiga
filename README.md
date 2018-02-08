## About
This is example Docker Compose file for running [Taiga](https://taiga.io) project management platform for agile developers, designers and project managers with taiga-events and ssl-enabled reverse proxy with all images based on alpine:latest.

## Basic usage
1) Clone this repository.
`git clone --depth=1 -b latest https://github.com/docker-taiga/taiga.git`
2) Create `cert` folder and put ssl certificate and key inside. Default names are `fullchain.pem` and `privkey.pem`. This can be changed by adding `CERT_NAME` and `CERT_KEY` environment variables to the service `proxy`. Alternatively, if you use certbot to acquire certificates, point volume `/taiga-cert` of the `proxy` service to the location of certificates, e.g. `/etc/letsencrypt/live/yourdomain.com`.
3) Adjust hostname, django secret and passwords for postgresql and rabbitmq.
4) `docker-compose up`

## Individual images
- **Taiga backend**
<https://github.com/docker-taiga/back>
[`docker pull dockertaiga/back`](https://hub.docker.com/r/dockertaiga/back/)
- **Taiga frontend**
<https://github.com/docker-taiga/front>
[`docker pull dockertaiga/front`](https://hub.docker.com/r/dockertaiga/front/)
- **RabbitMQ server**
<https://github.com/docker-taiga/rabbit>
[`docker pull dockertaiga/rabbit`](https://hub.docker.com/r/dockertaiga/rabbit/)
- **Taiga events**
<https://github.com/docker-taiga/events>
[`docker pull dockertaiga/events`](https://hub.docker.com/r/dockertaiga/events/)
- **Nginx reverse proxy**
<https://github.com/docker-taiga/proxy>
[`docker pull dockertaiga/proxy`](https://hub.docker.com/r/dockertaiga/proxy/)

## Environment variables

#### back
- **TAIGA_HOST** - Taiga hostname to use with this taiga setup.
- **TAIGA_SECRET** - Django secret key.
- **DB_HOST** - PostgeSQL hostname. Default is `db` service.
- **DB_NAME** - PostgeSQL database name. Default is same as `db::POSTGRES_DB`.
- **DB_USER** - PostgeSQL username. Default is same as `db::POSTGRES_USER`.
- **DB_PASSWORD** - PostgeSQL password. Default is same as `db::POSTGRES_PASSWORD`.
- **RABBIT_HOST** - RabbitMQ hostname. Default is `rabbit` service.
- **RABBIT_USER** - RabbitMQ username. Default is same as `rabbit::RABBIT_USER`.
- **RABBIT_PASSWORD** - RabbitMQ password. Default is same as `rabbit::RABBIT_PASSWORD`.
- **RABBIT_VHOST** - RabbitMQ virtual host name. Default is same as `rabbit::RABBIT_VHOST`.
- **STARTUP_TIMEOUT** - Time to wait for databse to become ready before creating schema and importing default data.

#### front
- **TAIGA_HOST** - Taiga hostname. Default is same as `back::TAIGA_HOST`.

#### db
- **POSTGRES_DB** - Database name.
- **POSTGRES_USER** - PostgreSQL username.
- **POSTGRES_PASSWORD** - PostgreSQL password.
*See [postgres image](https://hub.docker.com/_/postgres/) documentation for details.*

#### rabbit
- **RABBIT_USER** - RabbitMQ username.
- **RABBIT_PASSWORD** - RabbitMQ password.
- **RABBIT_VHOST** - RabbitMQ virtual host name.
- **STARTUP_TIMEOUT** - Time to wait for RabbitMQ server to become ready before creating user, vhost and assigning permissions.

#### events
- **RABBIT_HOST** - RabbitMQ hostname. Default is `rabbit` service.
- **RABBIT_USER** - RabbitMQ username. Default is same as `rabbit::RABBIT_USER`.
- **RABBIT_PASSWORD** - RabbitMQ password. Default is same as `rabbit::RABBIT_PASSWORD`.
- **RABBIT_VHOST** - RabbitMQ virtual host name. Default is same as `rabbit::RABBIT_VHOST`.

#### proxy
- **TAIGA_HOSTNAME** - Taiga hostname. Default is same as `back::TAIGA_HOST`.
- **TAIGA_BACK_HOST** - Backend hostname. Default is `back` service.
- **TAIGA_FRONT_HOST** - Frontend hostname. Default is `front` service.
- **EVENTS_HOST** - Events hostname. Default is `events` service.
- **CERT_NAME** - Name of certificate file. Default is `fullchain.pem`.
- **CERT_KEY** - Name of certificate key file. Default is `privkey.pem`.

## Configuration
By default configuration volume is `./conf` with config files `./conf/back/config.py` for backend, `./conf/front/config.json` for frontend and `./conf/proxy/nginx.conf` for reverse proxy. Generated config files are placed here on first run and can be modified to specify e.g. SMTP server configuration.

## Persistence
Volume `./data` contains postgresql data and taiga media files for persistence and backup purposes.
