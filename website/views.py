from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Truck

# Create your views here.




def index(request):
    return render(request, 'website/index.html', {})

def contact(request):
    return render(request, 'website/Contact_Us.html', {})

def map(request):
    return render(request, 'website/map.html', {})

#def detail(request, truck_id):
#    try:
#        truck = Truck.objects.get(pk=truck_id)
#    except Truck.DoesNotExist:
#        raise Http404("Truck does not exist")
#    return render(request, 'website/detail.html', {'truck': truck})
