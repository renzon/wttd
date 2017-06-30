from django.db import models
from django.shortcuts import resolve_url

from eventex.subscriptions.validators import validate_has_11_chars, \
    validate_digits_only


class Subscription(models.Model):
    name = models.CharField('nome', max_length=100)
    cpf = models.CharField(
        'CPF',
        max_length=11,
        validators=[validate_digits_only, validate_has_11_chars]
    )
    email = models.EmailField('email', blank=True)
    phone = models.CharField('telefone', blank=True, max_length=20)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    paid = models.BooleanField('Pago', default=False)

    class Meta:
        verbose_name = 'inscrição'
        verbose_name_plural = 'inscrições'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return resolve_url('subscriptions:detail', self.pk)
