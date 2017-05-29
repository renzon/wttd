from django.shortcuts import render

from eventex.subscriptions.forms import SubscriptionForm


def inscricao(request):
    ctx = {'form': SubscriptionForm()}
    return render(request, 'subscriptions/subscription_form.html', ctx)
