from django import forms


class SubscriptionForm(forms.Form):
    name = forms.CharField(label='Nome')
    cpf = forms.CharField(label='CPF')
    email = forms.EmailField()
    phone = forms.CharField(label='Telefone')
