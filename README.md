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

#### Surge Duration
##### Demand is a time-dependent concept, so the registered user can set dynamic time-window (```duration```) in minutes.
```console
curl --location --request POST 'http://localhost:8080/duration' \
--header 'Authorization: Bearer 'ACCESS TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{
    "duration": 10
}'
```

#### Threshold/Coefficients
##### Thresholds/Coefficients is configurable, so the registered user be able to modify them anytime. ```request_count``` is the number of requests that occur during time-window(duration) and ```coefficient``` is the coefficient of that requests.
```console
curl --location --request POST 'http://localhost:8080/threshold' \
--header 'Authorization: Bearer 'ACCESS TOKEN' \
--header 'Content-Type: application/json' \
--data-raw '{
    "request_count": 1000,
    "coefficient": 1.05
}'
```
