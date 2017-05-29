import pytest
from django.test import TestCase


@pytest.fixture()
def django_test_case():
    return TestCase()
