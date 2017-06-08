import pytest

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription

pytestmark = pytest.mark.django_db


@pytest.fixture()
def get_resp(client):
    return client.get('/inscricao/')


def test_get_status_code(get_resp):
    """Must return 200 HTTP status code"""
    assert 200 == get_resp.status_code


def test_get_template(get_resp):
    """Must use subscription_form.html"""
    assert ('subscriptions/subscription_form.html' ==
            get_resp.templates[0].name)


FORM_INPUTS = (
    ('<form', 1),
    ('<input', 6),
    ('type="text"', 3),
    ('type="email"', 1),
    ('type="submit"', 1)
)


@pytest.mark.parametrize('tag,occurrence', FORM_INPUTS)
def test_get_form_html(tag, occurrence, get_resp, django_test_case):
    """Must contain input tags"""
    django_test_case.assertContains(get_resp, tag, occurrence)


def test_get_form_csrf(get_resp, django_test_case):
    """Must contain CSRF token"""
    django_test_case.assertContains(get_resp, 'csrfmiddlewaretoken')


def test_form_in_context(get_resp):
    """Must contain SubscriptionForm instance on context"""
    assert isinstance(get_resp.context['form'], SubscriptionForm)


def test_post(django_test_case, post_resp):
    django_test_case.assertRedirects(post_resp, '/inscricao/1/')


def test_send_subscribe_email(outbox):
    assert 1 == len(outbox)


@pytest.mark.usefixtures('post_resp')
def test_save():
    assert Subscription.objects.exists()
