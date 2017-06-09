from django.conf.urls import url

from eventex.subscriptions.views import new, detail

urlpatterns = [
    url(r'ˆ$', new, name='new'),
    url(r'ˆ(\d+)/$', detail, name='detail'),
]
