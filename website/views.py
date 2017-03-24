from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from .models import Truck

# Create your views here.

def index(request):
    latest_truck_list = Truck.objects.all()
    context = {'latest_truck_list': latest_truck_list,}
    return render(request, 'website/index.html', context)

def truckslist(request):
    return HttpResponse("Looking at list of trucks")

def detail(request, truck_id):
    try:
        truck = Truck.objects.get(pk=truck_id)
    except Truck.DoesNotExist:
        raise Http404("Truck does not exist")
    return render(request, 'website/detail.html', {'truck': truck})
