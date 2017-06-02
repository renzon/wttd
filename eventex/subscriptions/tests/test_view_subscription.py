import pytest

from eventex.subscriptions.forms import SubscriptionForm


# Form GET tests

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


def test_form_fields():
    """Subscription Form must have 4 fields"""
    form = SubscriptionForm()
    assert 'name cpf email phone'.split() == list(form.fields)


# Form post tests


def test_post(post_resp):
    assert 302 == post_resp.status_code


def test_send_subscribe_email(outbox):
    assert 1 == len(outbox)


@pytest.fixture()
def error_resp(client):
    return client.post('/inscricao/', {})


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


def test_success_msg(client, post_data, django_test_case):
    """Test a successful subscritption"""
    resp = client.post('/inscricao/', post_data, follow=True)
    django_test_case.assertContains(resp, 'Inscrição realizada com sucesso!')
