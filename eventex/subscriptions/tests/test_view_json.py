import json

import pytest
from django.shortcuts import resolve_url


@pytest.fixture
def get_resp(client):
    return client.get(resolve_url('subscriptions:json_example'))


def test_get_status_code(get_resp):
    """Must return 200 HTTP status code"""
    assert 200 == get_resp.status_code


def test_json(get_resp):
    """Must return 200 HTTP status code"""
    json_str = get_resp.content
    dct = json.loads(json_str)
    expected = {
        "Books": "Books",
        "Games": "Games"
    }
    assert expected == dct
