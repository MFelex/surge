![pylint Score](https://mperlet.github.io/pybadge/badges/9.svg)
![Pytest Coverage](https://svgshare.com/i/d6Z.svg)
# surge
Determine the price coefficient based on the demand rate in Tehran districts
This service is designed for an online ride-hailing application so that in order to balance supply and demand, the price will increase when the number of requests in a district exceeds the set limit.
This service offers a price increase coefficient in REST API based on a configurable time-window and a threshold/coefficient table.
it divided into the following categories:
- [x] Register user to config time-window and treshold/coefficient
- [x] Add time-window (duration)
- [x] Add or delete threshold/coefficient
- [x] Provide coefficient based on latitude and longitude

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

#### Surge
##### The main service that return Tehran district ```coefficient``` based on ```latitude``` and ```longitude``` 
```console
curl --location --request GET 'http://localhost:8080/surge?lat=51.4096035&lon=35.7578398'
```
