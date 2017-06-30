from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscriptionCreate(CreateView):
    model = Subscription
    form_class = SubscriptionForm

    def form_valid(self, form):
        response = super().form_valid(form)
        self.send_email()
        return response

    def send_email(self):
        template = 'subscriptions/subscription_email.txt'
        subject = 'Confirmação de Inscrição'
        from_ = settings.DEFAULT_FROM_EMAIL
        to = self.object.email
        context = {'subscription': self.object}
        body = render_to_string(template, context)
        mail.send_mail(subject, body, from_, [from_, to])


new = SubscriptionCreate.as_view()

detail = DetailView.as_view(model=Subscription)
