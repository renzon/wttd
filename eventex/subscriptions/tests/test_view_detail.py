import pytest
from django.shortcuts import resolve_url

from eventex.subscriptions.models import Subscription
from eventex.subscriptions.tests.conftest import post_data

pytestmark = pytest.mark.django_db


@pytest.fixture()
def subscription(post_data):
    subs = Subscription(**post_data)
    subs.save()
    return subs


@pytest.fixture()
def get_resp(client, subscription):
    assert subscription  # used to avoid unused param
    return client.get(resolve_url('subscriptions:detail', subscription.pk))


def test_get_status_code(get_resp):
    """Must return 200 HTTP status code"""
    assert 200 == get_resp.status_code


def test_template(django_test_case, get_resp):
    django_test_case.assertTemplateUsed(
        get_resp,
        'subscriptions/subscription_detail.html'
    )


def test_context(get_resp):
    assert isinstance(get_resp.context['subscription'], Subscription)


@pytest.mark.parametrize('data', post_data().values())
def test_html(django_test_case, get_resp, data):
    django_test_case.assertContains(get_resp, data)


def test_not_existing_subscription(client):
    resp = client.get(resolve_url('subscriptions:detail', 0))
    assert 404 == resp.status_code
