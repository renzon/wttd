import pytest
from django.shortcuts import resolve_url

from eventex.core.models import Talk, Speaker, Course

pytestmark = pytest.mark.django_db


@pytest.fixture
def talk_list_get(client):
    activities = [
        Talk(title='Título da Palestra', start='10:00',
             description='Descrição da palestra.'),
        Talk(title='Título da Palestra', start='13:00',
             description='Descrição da palestra.'),
        Course(title='Título do Curso', start='9:00',
               description='Descrição do curso.', slots=20)
    ]
    speaker = Speaker.objects.create(
        name='Henrique Bastos',
        slug='henrique-bastos',
        website='//henriquebastos.net',
    )

    for a in activities:
        a.save()
        a.speakers.add(speaker)
    return client.get(resolve_url('talk_list'))


def test_get(talk_list_get):
    assert 200 == talk_list_get.status_code


def test_template(talk_list_get, django_test_case):
    django_test_case.assertTemplateUsed(talk_list_get, 'core/talk_list.html')


@pytest.mark.parametrize(
    'ocurrencies,content',
    [
        (2, 'Título da Palestra'),
        (3, 'Henrique Bastos'),
        (3, '/palestrantes/henrique-bastos'),
        (2, 'Descrição da palestra'),
        (1, '10:00'),
        (1, '13:00'),
        (1, 'Manhã'),
        (1, 'Tarde'),
        (1, 'Título do Curso'),
        (1, '9:00'),
        (1, 'Descrição do curso.'),
    ]
)
def test_content(talk_list_get, django_test_case, ocurrencies, content):
    django_test_case.assertContains(talk_list_get, content, ocurrencies)


@pytest.mark.parametrize('var', ['talk_list'])
def test_context(talk_list_get, var):
    context = talk_list_get.context
    assert var in context


@pytest.mark.parametrize(
    'msg',
    [
        'Ainda não existem palestras de manhã.',
        'Ainda não existem palestras de tarde.',
    ]
)
def test_empty_talk_list(client, django_test_case, msg):
    resp = client.get(resolve_url('talk_list'))
    django_test_case.assertContains(resp, msg)
