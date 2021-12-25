from django.urls import reverse


def test_register_user_url():
    path = reverse('register')
    assert path == '/user/register'


def test_register_login_url():
    path = reverse('login')
    assert path == '/user/login'


def test_threshold_url():
    path = reverse('threshold')
    assert path == '/threshold'


def test_threshold_detail_url():
    path = reverse('threshold-detail', args=[1])
    assert path == '/threshold/1'


def test_duration_url():
    path = reverse('duration')
    assert path == '/duration'


def test_surge_url():
    path = reverse('surge')
    assert path == '/surge'
