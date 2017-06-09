import pytest
from django.shortcuts import resolve_url


@pytest.fixture()
def post_data():
    return dict(name='Renzo Nuccitelli', cpf='12345678901',
                email='renzo@python.pro.br', phone='2345678')


@pytest.fixture()
def post_resp(client, post_data):
    return client.post(resolve_url('subscriptions:new'), post_data)


@pytest.fixture()
def outbox(post_resp, mailoutbox):
    assert post_resp  # is here only to proceed post call
    return mailoutbox
