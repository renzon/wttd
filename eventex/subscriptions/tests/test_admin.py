import pytest
from model_mommy import mommy

from eventex.subscriptions.admin import admin, Subscription, SubscriptioAdmin


@pytest.fixture
def subscriptions(db):
    return mommy.make(Subscription, paid=False, _quantity=4)


@pytest.fixture
def subscription_admin():
    return SubscriptioAdmin(Subscription, admin.site)


def test_has_mark_as_paid(subscription_admin: SubscriptioAdmin):
    """Check SubscriptionAdmin as mark_as_paid action"""
    assert 'mark_as_paid' in subscription_admin.actions


def test_mark_all_as_paid(subscriptions, subscription_admin: SubscriptioAdmin,
                          mocker):
    """Check all selected subscription are marked as paid"""
    subscription_admin.mark_as_paid(mocker.Mock(), Subscription.objects.all())
    assert len(subscriptions) == Subscription.objects.filter(paid=True).count()


@pytest.mark.usefixtures('subscriptions')
def test_success_msg(mocker, subscription_admin: SubscriptioAdmin):
    """Check success message is displayed"""
    mocker.spy(subscription_admin, 'message_user')
    subscription_admin.mark_as_paid(mocker.Mock(), Subscription.objects.all())
    assert 1 == subscription_admin.message_user.call_count
