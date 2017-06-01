import pytest

from eventex.subscriptions.forms import SubscriptionForm


# Form GET tests

@pytest.fixture()
def inscricao_get_resp(client):
    return client.get('/inscricao/')


def test_status_code(inscricao_get_resp):
    """Must return 200 HTTP status code"""
    assert 200 == inscricao_get_resp.status_code


def test_template(inscricao_get_resp):
    """Must use subscription_form.html"""
    assert ('subscriptions/subscription_form.html' ==
            inscricao_get_resp.templates[0].name)


def test_html(inscricao_get_resp, django_test_case):
    """Must contain input tags"""
    django_test_case.assertContains(inscricao_get_resp, '<form')
    django_test_case.assertContains(inscricao_get_resp, '<input', 6)
    django_test_case.assertContains(inscricao_get_resp, 'type="text"', 3)
    django_test_case.assertContains(inscricao_get_resp, 'type="email"')
    django_test_case.assertContains(inscricao_get_resp, 'type="submit"')


def test_csrf(inscricao_get_resp, django_test_case):
    """Must contain CSRF token"""
    django_test_case.assertContains(inscricao_get_resp, 'csrfmiddlewaretoken')


def test_form(inscricao_get_resp):
    """Must contain SubscriptionForm instance on context"""
    assert isinstance(inscricao_get_resp.context['form'], SubscriptionForm)


def test_form_fields():
    """Subscription Form must have 4 fields"""
    form = SubscriptionForm()
    assert 'name cpf email phone'.split() == list(form.fields)


# Form post tests


@pytest.fixture()
def inscricao_post_resp(client):
    data = dict(name='Renzo Nuccitelli', cpf='12345678901',
                email='renzon@gmail.com', phone='2345678')
    resp = client.post('/inscricao/', data)
    return resp


def test_positive_post(inscricao_post_resp):
    assert 302 == inscricao_post_resp.status_code


def test_send_subscribe_email(inscricao_post_resp, mailoutbox):
    assert 1 == len(mailoutbox)
    # inscricao_post_resp is here only to make a post request
    assert inscricao_post_resp
