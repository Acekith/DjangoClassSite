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
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import Truck
from .models import Menu_item
from .models import Location
from .models import Hours
import uuid
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

#    def post(self, request, *args, **kwargs):
#        if form.is_valid():
#            newPic = Pic(imgfile = request.FILES['imgfile'])
#            newPic.save()



    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            print request, args, kwargs, request.META, request.FILES
            newPic = request.FILES['truck_picture']
            default_storage.save(uuid.uuid4().hex, ContentFile(newpic.read()))
        else:
            return self.form_invalid(form)

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

#****************** CRUD for menu items************************

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
        # context["truck"]=Truck.objects.get(pk=self.kwargs["pk"])
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
    def get_success_url(self, **kwargs):
        return reverse('website:truck-menuitem-list', kwargs={'pk': self.truck_id})

    def delete(self, request, *args, **kwargs):
        truck = self.get_object().truck
        self.truck_id = truck.id
        return super(MenuItemDelete, self).delete(request, *args, **kwargs)

#******************CRUD for Locations******************

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
    fields =[
    'latitude',
    'longitude',
    'start_time',
    'end_time',
    'day',]

    template_name_suffix = '_update_form'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LocationItemUpdate, self).get_context_data(**kwargs)
        # Add in the publisher
        context["truck"]=Truck.objects.get(pk=self.kwargs["pk"])
        return context

class LocationCreate(CreateView):
    model = Location
    fields =[
    'latitude',
    'longitude',
    'start_time',
    'end_time',
    'day',]

    def form_valid(self, form):
        form.instance.truck = Truck.objects.get(pk=self.kwargs['pk_truck'])
        return super(LocationCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LocationCreate, self).get_context_data(**kwargs)
        # Add in the publisher
        context["truck"]=Truck.objects.get(pk=self.kwargs["pk_truck"])
        return context

class LocationDelete(DeleteView):
    model = Location

    def get_success_url(self, **kwargs):
        return reverse('website:truck-location-list', kwargs={'pk': self.truck_id})

    def delete(self, request, *args, **kwargs):
        truck = self.get_object().truck
        self.truck_id = truck.id
        return super(LocationDelete, self).delete(request, *args, **kwargs)

#************CRUD for Hours ****************

class HoursListView(ListView):
    model = Hours

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HoursListView, self).get_context_data(**kwargs)
        # Add in the publisher
        context["truck"]=Truck.objects.get(pk=self.kwargs["pk"])
        return context

class HoursItemUpdate(UpdateView):
    model = Hours
    fields =[
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday',]


    template_name_suffix = '_update_form'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HoursItemUpdate, self).get_context_data(**kwargs)
        # Add in the publisher
        context["truck"]=Truck.objects.get(pk=self.kwargs["pk"])
        return context

class HoursCreate(CreateView):
    model = Hours
    fields =[
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday',]

    def form_valid(self, form):
        form.instance.truck = Truck.objects.get(pk=self.kwargs['pk_truck'])
        return super(HoursCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HoursCreate, self).get_context_data(**kwargs)
        # Add in the publisher
        context["truck"]=Truck.objects.get(pk=self.kwargs["pk_truck"])
        return context

