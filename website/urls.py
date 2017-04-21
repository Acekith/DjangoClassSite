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

    url(r'^trucks/(?P<pk>[0-9]+)/menuitems/$', views.MenuItemListView.as_view(), name='truck-menuitem-list'),
    url(r'^trucks/(?P<pk_truck>[0-9]+)/menuitems/create/$', views.MenuItemCreate.as_view(), name='truck-menuitem-create'),
    url(r'^menuitems/(?P<pk>[0-9]+)/update/$', views.MenuItemUpdate.as_view(), name='truck-menuitem-update'),
    url(r'^menuitems/(?P<pk>[0-9]+)/delete/$', views.MenuItemDelete.as_view(), name='truck-menuitem-delete'),

    url(r'^trucks/(?P<pk>[0-9]+)/Locations/$', views.LocationListView.as_view(), name='truck-location-list'),
    url(r'^trucks/(?P<pk_truck>[0-9]+)/Locations/create/$', views.LocationCreate.as_view(), name='truck-location-create'),
    url(r'^locations/(?P<pk>[0-9]+)/update/$', views.LocationItemUpdate.as_view(), name='truck-location-update'),
    url(r'^locations/(?P<pk>[0-9]+)/delete/$', views.LocationDelete.as_view(), name='truck-location-delete'),
    # ex/map/
    url(r'^trucks/(?P<pk>[0-9]+)/hours/$', views.HoursListView.as_view(), name='truck-hours-list'),
    url(r'^trucks/(?P<pk_truck>[0-9]+)/hours/create/$', views.HoursCreate.as_view(), name='truck-hours-create'),
    url(r'^hours/(?P<pk>[0-9]+)/update/$', views.HoursItemUpdate.as_view(), name='truck-hours-update'),

    url(r'^map/$', views.map, name='map'),
    url(r'^contact/$', views.contact, name='contact'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
