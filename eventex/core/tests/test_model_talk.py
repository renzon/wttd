import pytest
from model_mommy import mommy

from eventex.core.managers import PeriodQuerySet
from eventex.core.models import Talk, Course

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


@pytest.fixture
def morning_talk():
    return mommy.make(Talk, start='11:59')


@pytest.fixture
def afternoon_talk():
    return mommy.make(Talk, start='12:00')


def test_manager():
    assert isinstance(Talk.objects.get_queryset(), PeriodQuerySet)


def test_morning_talk(morning_talk):
    assert [morning_talk] == list(Talk.objects.at_morning())


def test_afternoon_talk(afternoon_talk):
    assert [afternoon_talk] == list(Talk.objects.at_afternoon())


def test_ordering():
    assert ['start'] == Talk._meta.ordering


@pytest.fixture
def course():
    return Course.objects.create(
        title='Título do Curso',
        start='9:00',
        description='Descrição do curso.',
        slots=20
    )


@pytest.mark.usefixtures('course')
def test_course_create():
    assert Course.objects.exists()


def test_course_spekar(course):
    course.speakers.create(
        name='Henrique Bastos',
        slug='henrique-bastos',
        website='//henriquebastos.net',
    )
    assert 1 == course.speakers.count()


def test_course_str(course):
    assert course.title == str(course)


def test_course_manager():
    assert isinstance(Course.objects.get_queryset(), PeriodQuerySet)


def test_course_ordering():
    assert ['start'] == Course._meta.ordering
