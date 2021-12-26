![pylint Score](https://mperlet.github.io/pybadge/badges/9.svg)
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

## How to use the application
#### Register User
##### User has to enter ```Username```, ```email``` and ```password``` fields to register
```console
curl --location --request POST 'http://localhost:8080/user/register' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "John",
    "email": "JohnDou@gmail.com",
    "password": "NewPass12"
}'
```

#### Login User
##### User can login using ```username``` and ```password```. The reponse of this API is includes JWT ```access``` and ```refresh```.
```console
curl --location --request POST 'http://localhost:8080/user/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "John",
    "password": "NewPass12"
}'
```
