from datetime import datetime

import pytest

from eventex.subscriptions.models import Subscription

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
