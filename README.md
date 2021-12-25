# surge
Determine the price coefficient based on the demand rate in Tehran`s districts

## Built With
- [Python](https://www.python.org)
- [Django](https://www.djangoproject.com)
- [Django Rest Framework ](https://www.django-rest-framework.org)
- [PostgreSQL](https://www.postgresql.org) + [PostGIS](https://postgis.net)
- [Redis](https://redis.io)
- [Celery](https://docs.celeryproject.org/en/stable/)
- [Docker](https://www.docker.com)

## Run the application
You can run docker-compose and services like so:
```sh
$ git clone https://github.com/MFelex/surge.git
$ cd surge
$ mv settings.example.env settings.env
$ mv postgis.example.env postigs.env
$ docker-compose up -d
```
Now you can access Surge API at ```http://localhost:8080/``` from your host system.
