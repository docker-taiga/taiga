## About
This is example Docker Compose file for running [Taiga](https://taiga.io) project management platform for agile developers, designers and project managers with taiga-events and ssl-enabled reverse proxy with all images based on alpine:latest.

## Basic usage
1) Clone this repository.
`git clone --depth=1 -b latest https://github.com/docker-taiga/taiga.git`
2) Adjust hostname, django secret and passwords for postgresql and rabbitmq in `variables.env`.
2) (Optional) If you want to enable SSL, create `cert` folder and put ssl certificate and key inside. Default names are `fullchain.pem` and `privkey.pem`. This can be changed by adding `CERT_NAME` and `CERT_KEY` environment variables to the service `proxy`. Alternatively, if you use certbot to acquire certificates, point volume `/taiga-cert` of the `proxy` service to the location of certificates, e.g. `/etc/letsencrypt/live/yourdomain.com`.
4) `docker-compose up`

The default username and password taiga creates is `admin` with password `123123`.

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
###
- **TAIGA_HOST** - Taiga hostname to use with this taiga setup.
- **TAIGA_SCHEME** - Taiga URL scheme (http/https). Default is 'http'.
- **TAIGA_BACK_HOST** - Backend hostname. Default is `back` service.
- **TAIGA_FRONT_HOST** - Frontend hostname. Default is `front` service.
- **EVENTS_HOST** - Events hostname. Default is `events` service.
- **TAIGA_SECRET** - Django secret key.
###
- **ENABLE_SSL** - Enable SSL termination (yes/no). Default is 'yes'.
- **CERT_NAME** - Name of certificate file. Default is `fullchain.pem`.
- **CERT_KEY** - Name of certificate key file. Default is `privkey.pem`.
###
- **POSTGRES_HOST** - PostgeSQL hostname. Default is `db` service.
- **POSTGRES_DB** - Database name.
- **POSTGRES_USER** - PostgreSQL username.
- **POSTGRES_PASSWORD** - PostgreSQL password.
###
- **RABBIT_HOST** - RabbitMQ hostname. Default is `rabbit` service.
- **RABBIT_USER** - RabbitMQ username. Default is same as `rabbit::RABBIT_USER`.
- **RABBIT_PASSWORD** - RabbitMQ password. Default is same as `rabbit::RABBIT_PASSWORD`.
- **RABBIT_VHOST** - RabbitMQ virtual host name. Default is same as `rabbit::RABBIT_VHOST`.
###
- **STARTUP_TIMEOUT** - Time to wait for databse to become ready before creating schema and importing default data. Default is 15s.


## Configuration
By default configuration volume is `./conf` with config files `./conf/back/config.py` for backend, `./conf/front/config.json` for frontend and `./conf/proxy/nginx.conf` for reverse proxy. Generated config files are placed here on first run and can be modified to specify e.g. SMTP server configuration.

## Persistence
Volume `./data` contains postgresql data and taiga media files for persistence and backup purposes.

## Upgrading
*//TODO*
