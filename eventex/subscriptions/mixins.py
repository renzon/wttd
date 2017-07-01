from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.views.generic import CreateView


class EmailCreateMixin:
    email_subject = ''
    email_template_name = None
    email_context_name = None
    email_from = settings.DEFAULT_FROM_EMAIL
    email_to = None

    def send_email(self):
        template = self.get_email_template_name()
        subject = self.email_subject
        from_ = self.email_from
        to = self.get_email_to()
        context = self.get_email_context_data()
        body = render_to_string(template, context)
        mail.send_mail(subject, body, from_, [from_, to])

    def get_email_template_name(self):
        if self.email_template_name:
            return self.email_template_name
        meta = self.object._meta
        return f'{meta.app_label}/{meta.model_name}_email.txt'

    def get_email_context_data(self, **kwargs):
        context = dict(kwargs)
        context.update({self.get_email_context_name(): self.object})
        return context

    def get_email_context_name(self):
        if self.email_context_name:
            return self.email_context_name
        return self.object._meta.model_name

    def get_email_to(self):
        if self.email_to:
            return self.email_to
        return self.object.email


class EmailCreateView(EmailCreateMixin, CreateView):
    def form_valid(self, form):
        response = super().form_valid(form)
        self.send_email()
        return response
