import pytest
from django.shortcuts import resolve_url

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


@pytest.fixture()
def no_data_resp(client):
    return client.post(resolve_url('subscriptions:new'), {})


@pytest.fixture()
def no_email_and_phone_resp(client):
    data = dict(name='Renzo Nuccitelli', cpf='12345678901')
    return client.post(resolve_url('subscriptions:new'), data)


def test_error_status_code(no_data_resp):
    assert 200, no_data_resp.status_code


def test_error_template(no_data_resp):
    assert ('subscriptions/subscription_form.html' ==
            no_data_resp.templates[0].name)


def test_template_has_errors(no_email_and_phone_resp, django_test_case):
    """Check template has non fields errors"""
    django_test_case.assertContains(
        no_email_and_phone_resp, '<ul class="errorlist nonfield"')


def test_error_has_form(no_data_resp):
    assert isinstance(no_data_resp.context['form'], SubscriptionForm)


def test_error_has_msgs(no_data_resp):
    form = no_data_resp.context['form']
    assert form.errors


@pytest.mark.usefixtures('transactional_db', 'no_data_resp')
def test_negative_save():
    assert not Subscription.objects.exists()
