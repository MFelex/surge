import pytest
from model_bakery import baker
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.utils import timezone
from main.models import Threshold


@pytest.fixture()
def lat_lon():
    return {
        'lat': 51.123456789,
        'lon': 35.123456789,
    }


@pytest.fixture()
def user_info():
    return {
        'username': 'John',
        'email': 'JohnDou@gmail.com',
        'password': 'MyPass12',
    }


@pytest.fixture()
def threshold():
    return {
        'request_count': 1000,
        'coefficient': 1.05,
    }


@pytest.fixture()
def duration():
    return {
        'duration': 10,
    }


@pytest.fixture()
@pytest.mark.django_db
def token():
    user = User.objects.create(
        username='test',
        email='test@test.com',
        password='TestMe12',
    )
    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)
    return {
        'HTTP_AUTHORIZATION': f'Bearer {access}'
    }


@pytest.fixture()
@pytest.mark.django_db(transaction=True)
def threshold_db():
    threshold = Threshold.objects.create(
        request_count=1000,
        coefficient=1.05,
    )
    return threshold


@pytest.fixture()
@pytest.mark.django_db(transaction=True)
def requests_db():
    requested_time = timezone.now()
    return baker.make(
        'main.RequestDistrict',
        district=5,
        requested_time=requested_time,
        requested_count=100,
    )


@pytest.fixture()
@pytest.mark.django_db(transaction=True)
def coefficient_db():
    return baker.make(
        'main.Threshold',
        coefficient=1.05,
        request_count=1000,
    )
