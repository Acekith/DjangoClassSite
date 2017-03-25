from django.conf.urls import url

from . import views

app_name = 'website'
urlpatterns = [
    # ex: /website/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /website/5/
    url(r'^(?P<pk>[0-9]+)/$', views.TruckDetailView.as_view(), name='detail')

]

