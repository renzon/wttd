import pytest

from eventex.subscriptions.tests.conftest import post_data


@pytest.fixture
def email(outbox):
    return outbox[0]


def test_email_subject(email):
    assert 'Confirmação de Inscrição' == email.subject


def test_email_from(email):
    assert 'contato@eventex.com' == email.from_email


def test_email_to(email):
    assert ['contato@eventex.com', 'renzo@python.pro.br'] == email.to


@pytest.mark.parametrize('data', post_data().values())
def test_email_body(data, email):
    assert data in email.body