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


@pytest.mark.parametrize(
    'name,expected',
    [
        ('renzo nuccitelli', 'Renzo Nuccitelli'),
        ('RENZO NUCCITELLI', 'Renzo Nuccitelli'),
        ('ReNzO NuCcItElLi', 'Renzo Nuccitelli'),
        ('foo bar', 'Foo Bar'),
    ])
def test_capitalized_name(form: SubscriptionForm, name, expected):
    edit_and_validate(form, name=name)
    assert expected == form.cleaned_data['name']


@pytest.mark.parametrize('field', 'email phone'.split())
def test_optional_field(form, field):
    edit_and_validate(form, **{field: ''})
    assert {} == form.errors


@pytest.mark.parametrize(
    'email,expected',
    [
        ('', set(['__all__'])),
        ('invalid email', set('__all__ email'.split()))
    ])
def test_must_inform_email_or_phone(form, email, expected):
    """Email and Phone are optional, but at least one must be informed"""
    edit_and_validate(form, email=email, phone='')
    assert expected == set(form.errors)


def assert_field_error_code(form, field, error_code):
    errors = form.errors.as_data()
    errors_list = errors[field]
    exception = errors_list[0]
    assert error_code == exception.code


def edit_and_validate(form, **kwargs):
    form.data.update(kwargs)
    form.is_valid()
