from django.core import mail
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from eventex.subscriptions.forms import SubscriptionForm


def inscricao(request):
    if request.method == 'POST':
        mail.send_mail('Subject', 'Message', 'sender@email.com',
                       ['visitor@email.com'])
        return HttpResponseRedirect('/inscricao/')
    ctx = {'form': SubscriptionForm()}
    return render(request, 'subscriptions/subscription_form.html', ctx)
