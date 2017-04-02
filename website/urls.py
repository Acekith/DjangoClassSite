from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'website'
urlpatterns = [
    # ex: /website/
    url(r'^$', views.index, name='index'),
    # ex: /trucks/
    url(r'^trucks/$', views.TruckListView.as_view(), name='truck-list'),
    url(r'^trucks/create/$', views.TruckCreate.as_view(), name='truck-create'),
    # ex: /trucks/5/
    url(r'^trucks/(?P<pk>[0-9]+)/$', views.TruckDetailView.as_view(), name='truck-detail'),
    url(r'^trucks/(?P<pk>[0-9]+)/update/$', views.TruckUpdate.as_view(), name='truck-update'),
    url(r'^trucks/(?P<pk>[0-9]+)/delete/$', views.TruckDelete.as_view(), name='truck-delete'),
    # ex/map/
    url(r'^map/$', views.map, name='map'),
    url(r'^contact/$', views.contact, name='contact'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
