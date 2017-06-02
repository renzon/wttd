from eventex.subscriptions.forms import SubscriptionForm


def test_form_fields():
    """Subscription Form must have 4 fields"""
    form = SubscriptionForm()
    assert 'name cpf email phone'.split() == list(form.fields)
