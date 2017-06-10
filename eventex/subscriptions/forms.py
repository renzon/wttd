from django import forms
from django.core.exceptions import ValidationError


def validate_digits_only(cpf):
    if not cpf.isdigit():
        raise ValidationError('CPF deve conter apenas números', 'digits')


def validate_has_11_chars(cpf):
    if len(cpf) != 11:
        raise ValidationError('CPF deve conter exatamente 11 dígitos',
                              'length')


class SubscriptionForm(forms.Form):
    name = forms.CharField(label='Nome')
    cpf = forms.CharField(
        label='CPF',
        validators=[validate_digits_only, validate_has_11_chars])
    email = forms.EmailField()
    phone = forms.CharField(label='Telefone')

    def clean_name(self):
        name = self.cleaned_data['name']
        capitalized_names = map(str.capitalize, name.split())
        return ' '.join(capitalized_names)
