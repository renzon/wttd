import pytest

from eventex.subscriptions.forms import SubscriptionForm


@pytest.fixture()
def inscricao_resp(client):
    return client.get('/inscricao/')


def test_status_code(inscricao_resp):
    """Must return 200 HTTP status code"""
    assert 200 == inscricao_resp.status_code


def test_template(inscricao_resp):
    """Must use subscription_form.html"""
    assert ('subscriptions/subscription_form.html' ==
            inscricao_resp.templates[0].name)


def test_html(inscricao_resp, django_test_case):
    """Must contain input tags"""
    django_test_case.assertContains(inscricao_resp, '<form')
    django_test_case.assertContains(inscricao_resp, '<input', 6)
    django_test_case.assertContains(inscricao_resp, 'type="text"', 3)
    django_test_case.assertContains(inscricao_resp, 'type="email"')
    django_test_case.assertContains(inscricao_resp, 'type="submit"')


def test_csrf(inscricao_resp, django_test_case):
    """Must contain CSRF token"""
    django_test_case.assertContains(inscricao_resp, 'csrfmiddlewaretoken')


def test_form(inscricao_resp):
    """Must contain SubscriptionForm instance on context"""
    assert isinstance(inscricao_resp.context['form'], SubscriptionForm)


def test_form_fields():
    """Subscription Form must have 4 fields"""
    form = SubscriptionForm()
    assert 'name cpf email phone'.split() == list(form.fields)
