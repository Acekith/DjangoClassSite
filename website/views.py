from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Truck

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'website/index.html'
    context_object_name = 'latest_truck_list'

    def get_queryset(self):
        return Truck.objects.all()

class TruckDetailView(generic.DetailView):
    model = Truck
    template_name = 'website/truckdetail.html'




#def index(request):
#    latest_truck_list = Truck.objects.all()
#    context = {'latest_truck_list': latest_truck_list,}
#    return render(request, 'website/index.html', context)


#def detail(request, truck_id):
#    try:
#        truck = Truck.objects.get(pk=truck_id)
#    except Truck.DoesNotExist:
#        raise Http404("Truck does not exist")
#    return render(request, 'website/detail.html', {'truck': truck})
