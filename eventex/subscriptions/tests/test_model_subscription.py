from datetime import datetime

import pytest
from django.db import models
from django.shortcuts import resolve_url
from model_mommy import mommy

from eventex.subscriptions.models import Subscription, Country, City

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def subscription():
    subscription = Subscription(
        name='Renzo',
        cpf='12345678901',
        email='renzo@python.pro.br',
        phone='2345678'
    )
    subscription.save()
    return subscription


def test_create():
    assert Subscription.objects.exists()


def test_created_at(subscription):
    """Subscription must save da datetime it is created"""
    assert isinstance(subscription.created_at, datetime)


def test_str(subscription):
    assert 'Renzo' == str(subscription)


def test_default_paid(subscription):
    assert not subscription.paid


def test_get_absolute_url(subscription: Subscription):
    url = resolve_url('subscriptions:detail', subscription.pk)
    assert url == subscription.get_absolute_url()


def test_country_aggregation():
    country = mommy.make(Country)
    mommy.make(City, population=2, country=country)
    mommy.make(City, population=3, country=country)
    assert 5 == country.population


def test_countries_aggregation():
    brazil = mommy.make(Country, name='Brazil')
    mommy.make(City, population=4, country=brazil)
    mommy.make(City, population=5, country=brazil)

    usa = mommy.make(Country, name='United States')
    mommy.make(City, population=2, country=usa)
    mommy.make(City, population=3, country=usa)

    countries = list(Country.objects.order_by('name').annotate(total_population=models.Sum('city__population')))
    brasil_db, usa_db = countries
    assert brasil_db == brazil
    assert usa_db == usa
    assert 9 == brasil_db.total_population
    assert 5 == usa_db.total_population
