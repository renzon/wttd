from django.conf import settings
from django.contrib.messages import success
from django.core import mail
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def inscricao(request):
    if request.method == 'POST':
        return create(request)
    return new(request)


def new(request):
    ctx = {'form': SubscriptionForm()}
    return render(request, 'subscriptions/subscription_form.html', ctx)


def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        ctx = {'form': form}
        return render(request, 'subscriptions/subscription_form.html', ctx)

    _send_mail('subscriptions/subscription_email.txt',
               'Confirmação de Inscrição',
               settings.DEFAULT_FROM_EMAIL,
               form.cleaned_data['email'],
               form.cleaned_data)

    Subscription.objects.create(**form.cleaned_data)

    success(request, 'Inscrição realizada com sucesso!')
    return HttpResponseRedirect('/inscricao/')


def _send_mail(template, subject, from_, to, context):
    body = render_to_string(template, context)
    mail.send_mail(subject, body, from_, [from_, to])
