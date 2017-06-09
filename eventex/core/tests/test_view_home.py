import pytest
from django.shortcuts import resolve_url


@pytest.fixture()
def home_resp(client):
    return client.get(resolve_url('home'))


def test_home_status_code(home_resp):
    assert 200 == home_resp.status_code


def test_home_template(home_resp):
    assert 'index.html' == home_resp.templates[0].name


def test_subscription_link(home_resp, django_test_case):
    new_subscription = resolve_url('subscriptions:new')
    django_test_case.assertContains(home_resp, f'href="{new_subscription}"')
