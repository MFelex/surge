# pylint: disable=w613
from django.urls import reverse


def test_factor_view_should_pass(client, lat_lon, mocker):
    mocker.patch('main.views.find_district_by_database', return_value=1)
    mocker.patch('main.views.district_requests', return_value=1000)
    mocker.patch('main.views.find_coefficient', return_value=1.05)
    url = reverse('surge')
    res = client.get(url, data=lat_lon)
    assert res.json()['coefficient'] == 1.05
