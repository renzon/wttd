from django.core import mail
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from eventex.subscriptions.forms import SubscriptionForm


def inscricao(request):
    if request.method == 'POST':
        mail.send_mail(
            'Confirmação de Inscrição',
            'Message',
            'contato@eventex.com',
            ['contato@eventex.com', 'renzo@python.pro.br']
        )
        return HttpResponseRedirect('/inscricao/')
    ctx = {'form': SubscriptionForm()}
    return render(request, 'subscriptions/subscription_form.html', ctx)
