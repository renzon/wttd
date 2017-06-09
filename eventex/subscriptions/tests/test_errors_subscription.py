import pytest
from django.shortcuts import resolve_url

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


@pytest.fixture()
def error_resp(client):
    return client.post(resolve_url('subscriptions:new'), {})


def test_error_status_code(error_resp):
    assert 200, error_resp.status_code


def test_error_template(error_resp):
    assert ('subscriptions/subscription_form.html' ==
            error_resp.templates[0].name)


def test_error_has_form(error_resp):
    assert isinstance(error_resp.context['form'], SubscriptionForm)


def test_error_has_msgs(error_resp):
    form = error_resp.context['form']
    assert form.errors


@pytest.mark.usefixtures('transactional_db', 'error_resp')
def test_negative_save():
    assert not Subscription.objects.exists()
