from django.core.exceptions import ValidationError


def validate_digits_only(cpf):
    if not cpf.isdigit():
        raise ValidationError('CPF deve conter apenas números', 'digits')


def validate_has_11_chars(cpf):
    if len(cpf) != 11:
        raise ValidationError('CPF deve conter exatamente 11 dígitos',
                              'length')
