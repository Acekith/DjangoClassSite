from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from .models import Truck
from .models import Menu_item
from .models import Location
from .models import Hours

# Create your views here.




def index(request):
    return render(request, 'website/index.html', {})

def contact(request):
    return render(request, 'website/Contact_Us.html', {})

def map(request):
    trucks = Truck.objects.all()
    notrucks = all([x.whereami() is None for x in trucks])
    return render(request, 'website/map.html', {'trucks': trucks, 'notrucks': notrucks})

class TruckDetailView(DetailView):
    model = Truck

class TruckListView(ListView):
    model = Truck

class TruckCreate(CreateView):
    model = Truck
    fields = [
    'truck_name',
    'truck_picture',
    'truck_owner',
    'short_description',
    'description',]

class TruckUpdate(UpdateView):
    model = Truck
    fields = [
    'truck_name',
    'truck_picture',
    'short_description',
    'description',]
    template_name_suffix = '_update_form'


class TruckDelete(DeleteView):
    model = Truck
    success_url = reverse_lazy('truck-list')

# CRUD for menu items

class MenuItemListView(ListView):
    model = Menu_item

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MenuItemListView, self).get_context_data(**kwargs)
        # Add in the publisher
        context["truck"]=Truck.objects.get(pk=self.kwargs["pk"])
        return context

class MenuItemUpdate(UpdateView):
    model = Menu_item
    fields = [
    'item_name',
    'item_price',
    'item_description',]

    template_name_suffix = '_update_form'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MenuItemUpdate, self).get_context_data(**kwargs)
        # Add in the publisher
        context["truck"]=Truck.objects.get(pk=self.kwargs["pk"])
        return context

class MenuItemCreate(CreateView):
    model = Menu_item
    fields = [
    'item_name',
    'item_price',
    'item_description',]
    #success_url = reverse('website:truck-menuitem-list' pk_truck=truck.id)

    def form_valid(self, form):
        form.instance.truck = Truck.objects.get(pk=self.kwargs['pk_truck'])
        return super(MenuItemCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MenuItemCreate, self).get_context_data(**kwargs)
        # Add in the publisher
        context["truck"]=Truck.objects.get(pk=self.kwargs["pk_truck"])
        return context

class MenuItemDelete(DeleteView):
    model = Menu_item
    def success_url(self):
        return reverse('website:truck-menuitem-list', kwargs={'pk': self.object.truck.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        html = """
               <html>
                   <head>
                       <script>window.onunload = refreshParent; function refreshParent() {
                               window.opener.location.href=%s;
                               }
                       </script>
                   </head>
                   <body>
                   <h1>object deleted successfully</h1>
                   <button type="button" onclick="window.close()">OK</button>
                   </body>
               </html>
               """ % reverse('website:truck-menuitem-list',
                              kwargs={'pk': self.object.truck.id
                                      }
                              )
        super(MenuItemDelete, self).post(request, *args, **kwargs)
        return HttpResponse(html)

#CRUD for Locations

class LocationListView(ListView):
    model = Location

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LocationListView, self).get_context_data(**kwargs)
        # Add in the publisher
        context["truck"]=Truck.objects.get(pk=self.kwargs["pk"])
        return context

class LocationItemUpdate(UpdateView):
    model = Location
    #fields =

class LocationCreate(CreateView):
    model = Location

    def form_valid(self, form):
        form.instance.truck = Truck.objects.get(pk=self.kwargs['truck_id'])
        return super(LocationCreate, self).form_valid(form)

class LocationDelete(DeleteView):
    model = Location

#CRUD for Hours

class HoursListView(ListView):
    model = Location

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HoursListView, self).get_context_data(**kwargs)
        # Add in the publisher
        context["truck"]=Truck.objects.get(pk=self.kwargs["pk"])
        return context

class HoursItemUpdate(UpdateView):
    model = Hours
    #fields =

class HoursCreate(CreateView):
    model = Hours

    def form_valid(self, form):
        form.instance.truck = Truck.objects.get(pk=self.kwargs['truck_id'])
        return super(HoursCreate, self).form_valid(form)
