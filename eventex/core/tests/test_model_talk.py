import pytest

from eventex.core.models import Talk

pytestmark = pytest.mark.django_db


@pytest.fixture
def talk():
    return Talk.objects.create(
        title='Título da Palestra',
    )


@pytest.mark.usefixtures('talk')
def test_create():
    assert Talk.objects.exists()


def test_has_speakers(talk):
    talk.speakers.create(
        name='Henrique Bastos',
        slug='henrique-bastos',
        website='//henriquebastos.net',
    )
    assert 1 == talk.speakers.count()


@pytest.mark.parametrize('field_name', 'start description speakers'.split())
def test_blank_fields(field_name):
    field = Talk._meta.get_field(field_name)
    assert field.blank


def test_start_null():
    field = Talk._meta.get_field('start')
    assert field.null


def test_str(talk):
    assert 'Título da Palestra' == str(talk)
