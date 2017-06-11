from datetime import timedelta

import pytest
from django.utils.timezone import now
from model_mommy import mommy

from eventex.subscriptions.admin import admin, Subscription, SubscriptioAdmin


@pytest.fixture
def subscriptions(db):
    return mommy.make(Subscription, paid=False, _quantity=4)


@pytest.fixture
def subscription(db):
    return mommy.make(Subscription, paid=False)


@pytest.fixture
def subs_admin():
    return SubscriptioAdmin(Subscription, admin.site)


def test_has_mark_as_paid(subs_admin: SubscriptioAdmin):
    """Check SubscriptionAdmin as mark_as_paid action"""
    assert 'mark_as_paid' in subs_admin.actions


def test_mark_all_as_paid(subscriptions, subs_admin: SubscriptioAdmin,
                          mocker):
    """Check all selected subscription are marked as paid"""
    subs_admin.mark_as_paid(mocker.Mock(), Subscription.objects.all())
    assert len(subscriptions) == Subscription.objects.filter(paid=True).count()


@pytest.mark.usefixtures('subscriptions')
def test_success_msg_multi_subs(mocker, subs_admin: SubscriptioAdmin):
    """Check success message is displayed when multiple subscriptions are
    marked as paid
    """
    assert_message_user_called(mocker, subs_admin)


@pytest.mark.usefixtures('subscription')
def test_success_msg_single_subs(mocker, subs_admin: SubscriptioAdmin):
    """Check success message is displayed when single subscription is marked as
    paid
    """
    assert_message_user_called(mocker, subs_admin)


_now = now().today()


@pytest.mark.parametrize(
    'pay_date,expected',
    [
        (_now, True),
        (_now - timedelta(days=1), False),
        (_now - timedelta(days=2), False),
    ])
def test_subscribed_today(subs_admin, subscription, pay_date, expected):
    """Assert subscribed_today returns boolean accordingly with the date
    subscription were paid
    """
    subscription.created_at = pay_date
    assert subs_admin.subscribed_today(subscription) == expected


def assert_message_user_called(mocker, subs_admin):
    mocker.spy(subs_admin, 'message_user')
    subs_admin.mark_as_paid(mocker.Mock(), Subscription.objects.all())
    assert 1 == subs_admin.message_user.call_count
