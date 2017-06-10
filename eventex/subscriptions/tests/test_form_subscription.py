import pytest

from eventex.subscriptions.forms import SubscriptionForm


@pytest.fixture()
def form(post_data):
    form = SubscriptionForm(post_data)
    return form


def test_form_fields(form):
    """Subscription Form must have 4 fields"""
    assert 'name cpf email phone'.split() == list(form.fields)


@pytest.mark.parametrize('cpf', ['abcdefghijk', 'A1234567890', '1234567890@'])
def test_cpf_has_only_digits(form: SubscriptionForm, cpf):
    edit_and_validate(form, cpf=cpf)
    assert_field_error_code(form, 'cpf', 'digits')


@pytest.mark.parametrize('cpf', ['1234567890', '123456789', '12345678'])
def test_cpf_has_11_digits(form: SubscriptionForm, cpf):
    edit_and_validate(form, cpf=cpf)
    assert_field_error_code(form, 'cpf', 'length')


def assert_field_error_code(form, field, error_code):
    errors = form.errors.as_data()
    errors_list = errors[field]
    exception = errors_list[0]
    assert error_code == exception.code


def edit_and_validate(form, cpf):
    form.data['cpf'] = cpf
    form.is_valid()
