import pytest
from django.core.exceptions import ValidationError
from model_mommy import mommy

from eventex.core.models import Speaker, Contact

pytestmark = pytest.mark.django_db


@pytest.fixture
def speaker():
    return mommy.make(Speaker)


valid_kinds = pytest.mark.parametrize(
    'kind,value',
    [
        (Contact.EMAIL, 'renzo@python.pro.br'),
        (Contact.PHONE, '12-2345678')
    ]
)


@valid_kinds
def test_valid_choices(speaker, kind, value):
    Contact.objects.create(
        speaker=speaker,
        kind=kind,
        value=value
    )

    assert Contact.objects.exists()


@pytest.mark.parametrize(
    'kind,value',
    [
        ('X', 'invalid'),
        ('Y', 'another-invalid')
    ]
)
def test_invalid_choices(speaker, kind, value):
    """Contact kind must be 'E' for Email or 'P' for Phone"""
    contact = Contact.objects.create(
        speaker=speaker,
        kind=kind,
        value=value
    )
    pytest.raises(ValidationError, contact.full_clean)


@valid_kinds
def test_str(speaker, kind, value):
    contact = Contact(
        speaker=speaker,
        kind=kind,
        value=value
    )

    assert value == str(contact)
