from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from .models import Truck

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

class TruckDelete(DeleteView):
    model = Truck
    success_url = reverse_lazy('truck-list')
