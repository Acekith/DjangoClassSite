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
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
#from collection.forms import ContactForm
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Truck
from .models import Menu_item
from .models import Location
from .models import Hours
import uuid
# Create your views here.




def index(request):
    return render(request, 'website/index.html', {})

def comingsoon(request):
    return render(request, 'website/Coming_soon.html', {})

class ContactForm(forms.Form):

    fname = forms.CharField(
        label="First Name",
        max_length=64,
        widget=forms.TextInput(),
        required=True
    )
    lname = forms.CharField(
        label="Last Name",
        max_length=64,
        widget=forms.TextInput(),
        required=True
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(),
        required=True
    )
    phone = forms.RegexField(
        regex=r'^\+?1?\d{9,15}$',
        error_message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
        label="Telephone Number",
        max_length=64,
        widget=forms.TextInput(),
        required=True
    )
    message = forms.CharField(
        label="message",
        widget=forms.Textarea(),
        required=True
    )

def contact(request):
    #messages.add_message(request, messages.INFO, 'Hello world.')
    #messages.add_message(request, messages.SUCCESS, 'Hello world.')
    #messages.add_message(request, messages.WARNING, 'Hello world.')
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # do the email
            send_mail(
                "Truckie's Trucks feedback",
                form.cleaned_data["message"],
                "Truckie's Trucks <truckbot@grayson.hx42.org>",
                [
                    "gmiller@tamu.edu"
                ]
            )
            print form
            messages.add_message(request, messages.SUCCESS, 'Thank you for your feedback!')
            return HttpResponseRedirect('/')
        else:
            return render(request, 'website/contact.html', {
                'form': form,
            })
    else:
        form = ContactForm()

    return render(request, 'website/contact.html', {
        'form': form,
    })

def submit_order(request, pk):
    form_items = request.POST.keys()
    form_items.remove('csrfmiddlewaretoken')
    form_itmes = [int(x) for x in form_items]
    items_ordered = Menu_item.objects.all().filter(id__in=form_items)
    truck = Truck.objects.get(id=pk)
    user = request.user
    truckemail = truck.truck_owner.email
    useremail = user.email
    print items_ordered
    if len(items_ordered) > 0:
        message = "Thank you for your Order! \n"
        message+= truck.truck_name
        message+= "\n"
        message+= "\n"
        for item in items_ordered:
            message+= item.item_name
            message+= ":  $"
            message+= str(item.item_price)
            message+= "\n"
        message+= "\n"
        message+= "Your order will be ready soon!"
        send_mail(
            "Truckie's Trucks order",
            message,
            "Truckie's Trucks <truckbot@grayson.hx42.org>",
            [
                truckemail,
                useremail,
            ]
        )
        messages.add_message(request, messages.SUCCESS, 'Thank you! Your order has been recieved.')
    else:
        messages.add_message(request, messages.SUCCESS, 'Please select an item before submitting your order.')
    return HttpResponseRedirect('/trucks/%s/' % truck.id)
    # return reverse('website:truck-detail', kwargs={'pk': truck.id})

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
    'short_description',
    'description',]

    def get_success_url(self):
        return reverse_lazy('website:truck-update',args=(self.object.id,))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.truck_owner = self.request.user
        self.object.save()
        return super(TruckCreate, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            if 'truck_picture' in request.FILES:
                newpic = request.FILES['truck_picture']
                default_storage.save(uuid.uuid4().hex, ContentFile(newpic.read()))
            return self.form_valid(form)
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

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.truck_owner = self.request.user
        self.object.save()
        return super(TruckUpdate, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            #print request.FILES
            if 'truck_picture' in request.FILES:
                newpic = request.FILES['truck_picture']
                default_storage.save(uuid.uuid4().hex, ContentFile(newpic.read()))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class TruckDelete(DeleteView):
    model = Truck
    success_url = reverse_lazy('website:truck-list')

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

