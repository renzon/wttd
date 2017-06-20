from django import forms
from django.core.exceptions import ValidationError

from eventex.subscriptions.models import Subscription


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = 'name cpf email phone'.split()

    def clean_name(self):
        name = self.cleaned_data['name']
        capitalized_names = map(str.capitalize, name.split())
        return ' '.join(capitalized_names)

    def clean(self):
        self.cleaned_data = super().clean()
        optional_fields = map(self.cleaned_data.get, 'email phone'.split())
        if not any(optional_fields):
            raise ValidationError('Informe seu email ou telefone')
        return self.cleaned_data
