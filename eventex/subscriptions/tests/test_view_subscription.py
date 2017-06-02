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
def success_post_data():
    data = dict(name='Renzo Nuccitelli', cpf='12345678901',
                email='renzo@python.pro.br', phone='2345678')
    return data


@pytest.fixture()
def inscricao_post_resp(client, success_post_data):
    resp = client.post('/inscricao/', success_post_data)
    return resp


@pytest.fixture()
def outbox(inscricao_post_resp, mailoutbox):
    assert inscricao_post_resp  # is here only to proceed post call
    return mailoutbox


def test_positive_post(inscricao_post_resp):
    assert 302 == inscricao_post_resp.status_code


def test_send_subscribe_email(outbox):
    assert 1 == len(outbox)


def test_email_subject(outbox):
    email = outbox[0]
    assert 'Confirmação de Inscrição' == email.subject


def test_email_from(outbox):
    email = outbox[0]
    assert 'contato@eventex.com' == email.from_email


def test_email_to(outbox):
    email = outbox[0]
    assert ['contato@eventex.com', 'renzo@python.pro.br'] == email.to


def test_email_body(outbox):
    email = outbox[0]
    assert 'Renzo Nuccitelli' in email.body
    assert '2345678901' in email.body
    assert '2345678' in email.body
    assert 'renzo@python.pro.br' in email.body


@pytest.fixture()
def error_resp(client):
    return client.post('/inscricao/', {})


def test_error(error_resp):
    assert 200, error_resp.status_code


def test_error_template(error_resp):
    assert ('subscriptions/subscription_form.html' ==
            error_resp.templates[0].name)


def test_error_has_form(error_resp):
    assert isinstance(error_resp.context['form'], SubscriptionForm)


def test_error_msgs(error_resp):
    form = error_resp.context['form']
    assert form.errors


# success subscriptions

def test_success_msg(client, success_post_data, django_test_case):
    resp = client.post('/inscricao/', success_post_data, follow=True)
    django_test_case.assertContains(resp, 'Inscrição realizada com sucesso!')
