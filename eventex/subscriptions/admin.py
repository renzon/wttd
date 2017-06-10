from django.contrib import admin
from django.utils.timezone import now

from eventex.subscriptions.models import Subscription


class SubscriptioAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'cpf', 'phone', 'created_at', 'subscribed_today',
        'paid')
    date_hierarchy = 'created_at'
    search_fields = ('name', 'email', 'cpf', 'phone', 'created_at')
    list_filter = ('paid', 'created_at',)
    actions = ['mark_as_paid']

    def subscribed_today(self, subscription):
        return subscription.created_at.date() == now().date()

    subscribed_today.short_description = 'inscrito hoje?'
    subscribed_today.boolean = True

    def mark_as_paid(self, request, queryset):
        count = queryset.update(paid=True)
        if count == 1:
            msg = f'{count} inscrição foi marcada como paga'
        else:
            msg = f'{count} inscrições foram marcadas como pagas'
        self.message_user(request, msg)

    mark_as_paid.short_description = 'Marcar como pago'


admin.site.register(Subscription, SubscriptioAdmin)
