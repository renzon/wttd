from django.contrib.messages import success
from django.core import mail
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm


def inscricao(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.full_clean()
            body = render_to_string(
                'subscriptions/subscription_email.txt', form.cleaned_data)

            mail.send_mail(
                'Confirmação de Inscrição',
                body,
                'contato@eventex.com',
                ['contato@eventex.com', form.cleaned_data['email']]
            )
            success(request, 'Inscrição realizada com sucesso!')
            return HttpResponseRedirect('/inscricao/')

        ctx = {'form': form}
        return render(request, 'subscriptions/subscription_form.html', ctx)
    ctx = {'form': SubscriptionForm()}
    return render(request, 'subscriptions/subscription_form.html', ctx)
