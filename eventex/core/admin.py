# Register your models here.
from django.contrib import admin

from eventex.core.models import Speaker, Contact, Talk, Course


class ContactInline(admin.TabularInline):
    extra = 1
    model = Contact


class SpeakerModelAdmin(admin.ModelAdmin):
    inlines = [ContactInline]
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'photo_img', 'website_link', 'email', 'phone']

    def website_link(self, speaker):
        return f'<a href="{speaker.website}">{speaker.website}</a>'

    website_link.allow_tags = True
    website_link.short_descriptions = 'website'

    def photo_img(self, speaker):
        return f'<img src="{speaker.photo}" width="32px"/>'

    photo_img.allow_tags = True
    photo_img.short_descriptions = 'foto'

    def email(self, speaker):
        return speaker.contact_set.emails().first()

    def phone(self, speaker):
        return speaker.contact_set.phones().first()

    phone.short_description = 'telefone'


admin.site.register(Speaker, SpeakerModelAdmin)
admin.site.register(Talk)
admin.site.register(Course)
