import pytest
from django.core.management import call_command
from django.shortcuts import resolve_url

pytestmark = pytest.mark.django_db


@pytest.fixture(scope='session', autouse=True)
def django_db_setup(django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'eventex/core/fixtures/keynotes.json')


@pytest.fixture()
def home_resp(client):
    return client.get(resolve_url('home'))


def test_home_status_code(home_resp):
    assert 200 == home_resp.status_code


def test_home_template(home_resp):
    assert 'index.html' == home_resp.templates[0].name


def test_subscription_link(home_resp, django_test_case):
    new_subscription = resolve_url('subscriptions:new')
    django_test_case.assertContains(home_resp, f'href="{new_subscription}"')


@pytest.mark.parametrize(
    'content',
    [

        'Grace Hopper',
        'href="{}"'.format(resolve_url('speaker_detail', slug='grace-hopper')),
        '//hbn.link/hopper-pic',
        'Alan Turing',
        'href="{}"'.format(resolve_url(
            'speaker_detail', slug='alan-turing')),
        '//hbn.link/turing-pic'
    ]
)
def test_keynote_speakers(django_test_case, home_resp, content):
    """Test keynotes are present on home page"""
    django_test_case.assertContains(home_resp, content)


def test_speakers_link(django_test_case, home_resp):
    """Test speakers link is present on home page"""
    path = resolve_url('home')
    link = f'href="{path}#speakers"'
    django_test_case.assertContains(home_resp, link)
