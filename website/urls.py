from django.conf.urls import url

from . import views
urlpatterns = [
    # ex: /website/
    url(r'^$', views.index, name='index'),
    # ex: /website/truckslist/
    url(r'^truckslist/$', views.truckslist, name='trucklist'),
    # ex: /website/5/
    url(r'^(?P<truck_id>[0-9]+)/$', views.detail, name='detail')

]

