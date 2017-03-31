from django.conf.urls import url

from . import views

app_name = 'website'
urlpatterns = [
    # ex: /website/
    url(r'^$', views.index, name='index'),
    # ex: /website/5/
    #url(r'^(?P<pk>[0-9]+)/$', views.TruckDetailView.as_view(), name='detail')
    # ex/map/
    url(r'^map/$', views.map, name='map'),
    url(r'^contact/$', views.contact, name='contact'),

]

