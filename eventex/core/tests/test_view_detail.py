import pytest
from django.shortcuts import resolve_url

from eventex.core.models import Speaker

pytestmark = pytest.mark.django_db


@pytest.fixture
def detail_get(client):
    Speaker.objects.create(
        name='Grace Hopper',
        slug='grace-hopper',
        photo='//hbn.link/hopper-pic',
        website='//hbn.link/hopper-site',
        description='Programadora e almirante.'
    )
    return client.get(resolve_url('speaker_detail', slug='grace-hopper'))


def test_get(detail_get):
    assert 200 == detail_get.status_code


def test_template(detail_get, django_test_case):
    django_test_case.assertTemplateUsed(detail_get, 'core/speaker_detail.html')


@pytest.mark.parametrize(
    'content',
    [
        'Grace Hopper',
        'Programadora e almirante.',
        '//hbn.link/hopper-pic',
        '//hbn.link/hopper-site',
    ]
)
def test_html(detail_get, django_test_case, content):
    django_test_case.assertContains(detail_get, content)


def test_context(detail_get):
    speaker = detail_get.context['speaker']
    assert isinstance(speaker, Speaker)


def test_not_found(client):
    response = client.get(resolve_url('speaker_detail', slug='not-found'))
    assert 404 == response.status_code
