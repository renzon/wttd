from django.conf.urls import url
from django.contrib import admin

from eventex.core.views import home
from eventex.subscriptions.views import inscricao, detail

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^inscricao/$', inscricao),
    url(r'^inscricao/(\d+)/$', detail),
    url(r'^admin/', admin.site.urls),
]
