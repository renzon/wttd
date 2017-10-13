import json

from django.http import HttpResponse
from django.views.generic.detail import DetailView

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.mixins import EmailCreateView
from eventex.subscriptions.models import Subscription

new = EmailCreateView.as_view(
    email_subject='Confirmação de Inscrição',
    model=Subscription,
    form_class=SubscriptionForm
)

detail = DetailView.as_view(model=Subscription)


def json_example(request):
    to_json = {
        "Books": "Books",
        "Games": "Games"
    }
    return HttpResponse(json.dumps(to_json), content_type='application/json')
