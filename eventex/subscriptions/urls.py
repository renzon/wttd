from django.conf.urls import url

from eventex.subscriptions.views import new, detail, json_example

urlpatterns = [
    url(r'^$', new, name='new'),
    url(r'^json$', json_example, name='json_example'),
    url(r'^(?P<pk>\d+)/$', detail, name='detail'),
]
