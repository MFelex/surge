# pylint: disable=w613
import pytest
from rest_framework.test import APIClient
from django.urls import reverse


def test_factor_view_should_pass(client, lat_lon, mocker):
    mocker.patch('main.views.find_district_by_database', return_value=1)
    mocker.patch('main.views.district_requests', return_value=1000)
    mocker.patch('main.views.find_coefficient', return_value=1.05)
    url = reverse('surge')
    res = client.get(url, data=lat_lon)
    assert res.status_code == 200
    assert res.json()['coefficient'] == 1.05


@pytest.mark.django_db
def test_register_view_should_pass(client, user_info):
    url = reverse('register')
    res = client.post(url, data=user_info)
    assert res.status_code == 201


@pytest.mark.django_db
def test_post_surge_duration_should_pass(duration, mocker, token):
    mocker.patch('main.views.set_redis_surge_duration', return_value=None)
    url = reverse('duration')
    client = APIClient()
    client.credentials(**token)
    res = client.post(url, data=duration)
    assert res.status_code == 201


@pytest.mark.django_db
def test_get_surge_duration_should_pass(mocker, token):
    mocker.patch('main.views.set_redis_surge_duration', return_value=10)
    url = reverse('duration')
    client = APIClient()
    client.credentials(**token)
    res = client.get(url)
    assert res.status_code == 200
    assert res.json() == {'message': f'surge time set for last {10} minutes'}


@pytest.mark.django_db
def test_post_threshold_coefficient_should_pass(threshold, token):
    url = reverse('threshold')
    client = APIClient()
    client.credentials(**token)
    res = client.post(url, data=threshold)
    assert res.status_code == 201


@pytest.mark.django_db
def test_get_threshold_coefficient_should_pass(token, threshold_db):
    url = reverse('threshold')
    client = APIClient()
    client.credentials(**token)
    res = client.get(url)
    assert res.status_code == 200
    assert res.json() == [{'request_count': threshold_db.request_count, 'coefficient': threshold_db.coefficient}]


@pytest.mark.django_db(transaction=True)
def test_delete_threshold_coefficient_should_pass(threshold_db, token):
    url = reverse('threshold-detail', args=[threshold_db.id])
    client = APIClient()
    client.credentials(**token)
    res = client.delete(url)
    assert res.status_code == 204
