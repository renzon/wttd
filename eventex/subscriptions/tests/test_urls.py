from django.urls import reverse


def test_reverse():
    assert '/inscricao/' == reverse('subscriptions:new')
