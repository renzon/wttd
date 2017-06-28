import pytest
from django.shortcuts import resolve_url

from eventex.core.models import Speaker

pytestmark = pytest.mark.django_db


@pytest.fixture
def speaker():
    return Speaker.objects.create(name='Grace Hopper', slug='grace-hopper',
                                  photo='//hbn.link/hopper-pic',
                                  website='//hbn.link/hopper-site',
                                  description='Programadora e almirante.')


def test_create(speaker):
    assert speaker
    assert Speaker.objects.exists()


@pytest.mark.parametrize('field_name', ['description', 'website'])
def test_blank_fields(field_name):
    field = Speaker._meta.get_field(field_name)
    assert field.blank


def test_str(speaker):
    assert 'Grace Hopper' == str(speaker)


def test_get_absolute_url(speaker: Speaker):
    url = resolve_url('speaker_detail', slug=speaker.slug)
    assert url == speaker.get_absolute_url()
