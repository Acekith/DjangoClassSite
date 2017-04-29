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



# renders the index page
def index(request):
    return render(request, 'website/index.html', {})

#renders the coming soon page
def comingsoon(request):
    return render(request, 'website/Coming_soon.html', {})

# creates the form  on the contact page
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
    # EmailField auto checks for email formatting and prompts for formatting correction upon submission.
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(),
        required=True
    )
    # phone field uses RegexField type to check that the input is properly formatted as a phone number.
    # returns the error message if not formatted correctly.
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
# renders the contact page
def contact(request):
    # overwriting of POST method to call the sending of email once the submit button has been clicked.
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
            # Thanks the user for their for their feedback
            messages.add_message(request, messages.SUCCESS, 'Thank you for your feedback!')
            return HttpResponseRedirect('/')
        else:
            return render(request, 'website/contact.html', {
                'form': form,
            })
    else:
        form = ContactForm()

    # returns user to contact page once feedback is submitted
    return render(request, 'website/contact.html', {
        'form': form,
    })

# global function that handles the submission of orders from a specific truck's page
def submit_order(request, pk):
    # gets the items checked on the page
    form_items = request.POST.keys()
    #cleans the csrf token from the POST data
    form_items.remove('csrfmiddlewaretoken')
    form_itmes = [int(x) for x in form_items]
    items_ordered = Menu_item.objects.all().filter(id__in=form_items)
    #gets truck that is currently displayed
    truck = Truck.objects.get(id=pk)
    #sets the values for the emails to be sent to
    user = request.user
    truckemail = truck.truck_owner.email
    useremail = user.email
    #send the email to the truck owner and to the user
    if len(items_ordered) > 0:
        #builds message text
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
        #sends the email
        send_mail(
            "Truckie's Trucks order",
            message,
            "Truckie's Trucks <truckbot@grayson.hx42.org>",
            [
                truckemail,
                useremail,
            ]
        )
        #feedback to user
        messages.add_message(request, messages.SUCCESS, 'Thank you! Your order has been recieved.')
    else:
        #feedback to user
        messages.add_message(request, messages.SUCCESS, 'Please select an item before submitting your order.')
    return HttpResponseRedirect('/trucks/%s/' % truck.id)

#renders map page
def map(request):
    #gets the trucks objects to pass to the map
    trucks = Truck.objects.all()
    notrucks = all([x.whereami() is None for x in trucks])
    return render(request, 'website/map.html', {'trucks': trucks, 'notrucks': notrucks})

# renders detail view for each truck
class TruckDetailView(DetailView):
    model = Truck

# renders the list view that shows each truck
class TruckListView(ListView):
    model = Truck

# renders the create a truck page
class TruckCreate(CreateView):
    model = Truck
    # selection of fields to show up on page
    fields = [
    'truck_name',
    'truck_picture',
    'short_description',
    'description',]

    # sends user to the update page once truck has been created. passes the id of the truck to the update view
    def get_success_url(self):
        return reverse_lazy('website:truck-update',args=(self.object.id))

    # overwrites for_valid function to save the user id to the truck_owner field of the created truck
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.truck_owner = self.request.user
        self.object.save()
        return super(TruckCreate, self).form_valid(form)

    # overwrite POST method to save the image uploaded by the user to disk
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            if 'truck_picture' in request.FILES:
                newpic = request.FILES['truck_picture']
                # saving of picture with unique file name to disk occurs here
                default_storage.save(uuid.uuid4().hex, ContentFile(newpic.read()))
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

# renders update page for truck
class TruckUpdate(UpdateView):
    model = Truck
    # field selection
    fields = [
    'truck_name',
    'truck_picture',
    'short_description',
    'description',]
    template_name_suffix = '_update_form'

    # overwrite for_valid to ensure that the truck is saved with the correct owner id
    def form_valid(self, form):
       self.object = form.save(commit=False)
       self.object.truck_owner = self.request.user
       self.object.save()
       return super(TruckUpdate, self).form_valid(form)

    # overwrite post method to get the current truck and save the updated image to disk if it has been changed.
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.object = self.get_object()

        if form.is_valid():
            #print request.FILES
            if 'truck_picture' in request.FILES:
                newpic = request.FILES['truck_picture']
                # saving of image to disk happens here
                default_storage.save(uuid.uuid4().hex, ContentFile(newpic.read()))
        return super(TruckUpdate, self).post(request, *args, **kwargs)

# rendering of truck delete page
class TruckDelete(DeleteView):
    model = Truck
    success_url = reverse_lazy('website:truck-list')

#****************** CRUD for menu items************************

# rendering of list of menu items for each truck
class MenuItemListView(ListView):
    model = Menu_item

    # gets the current truck so the menu items displayed are only for that truck
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MenuItemListView, self).get_context_data(**kwargs)
        # Add in the truck
        context["truck"]=Truck.objects.get(pk=self.kwargs["pk"])
        return context

# renders update page for a single menu item
class MenuItemUpdate(UpdateView):
    model = Menu_item
    # field selection
    fields = [
    'item_name',
    'item_price',
    'item_description',]

    template_name_suffix = '_update_form'

    # gets the current truck so the edited item is saved to the correct truck and all the namespaced urls work
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MenuItemUpdate, self).get_context_data(**kwargs)
        return context

# renders the creation page for a menu item
class MenuItemCreate(CreateView):
    model = Menu_item
    # field selection
    fields = [
    'item_name',
    'item_price',
    'item_description',]

    # saves item to current truck
    def form_valid(self, form):
        form.instance.truck = Truck.objects.get(pk=self.kwargs['pk_truck'])
        return super(MenuItemCreate, self).form_valid(form)


    # gets the current truck so the edited item is saved to the correct truck and all the namespaced urls work
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MenuItemCreate, self).get_context_data(**kwargs)
        # Add in the truck
        context["truck"]=Truck.objects.get(pk=self.kwargs["pk_truck"])
        return context

# renders the deletion page for the menu items
class MenuItemDelete(DeleteView):
    model = Menu_item

    # returns user to menu item list page for their truck upon sucessful updating of an item
    def get_success_url(self, **kwargs):
        return reverse('website:truck-menuitem-list', kwargs={'pk': self.truck_id})

    # deletes the menu item from the truck
    def delete(self, request, *args, **kwargs):
        truck = self.get_object().truck
        self.truck_id = truck.id
        return super(MenuItemDelete, self).delete(request, *args, **kwargs)

#******************CRUD for Locations******************

# renders the location list page for the truck
class LocationListView(ListView):
    model = Location

    # gets the truck information to be passed to the page as well
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LocationListView, self).get_context_data(**kwargs)
        # Add in the truck
        context["truck"]=Truck.objects.get(pk=self.kwargs["pk"])
        return context

# renders the update page for the specified location
class LocationItemUpdate(UpdateView):
    model = Location
    # field selection
    fields =[
    'latitude',
    'longitude',
    'start_time',
    'end_time',
    'day',]

    template_name_suffix = '_update_form'

    # gets the truck information to be passed to the page as well
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LocationItemUpdate, self).get_context_data(**kwargs)
        return context

# renders the create a location page
class LocationCreate(CreateView):
    model = Location
    # field selection
    fields =[
    'latitude',
    'longitude',
    'start_time',
    'end_time',
    'day',]

    # saves the location with the id of the current truck as its owner. location.truck = truck.id
    def form_valid(self, form):
        form.instance.truck = Truck.objects.get(pk=self.kwargs['pk_truck'])
        return super(LocationCreate, self).form_valid(form)

    # gets the truck informationn to be passed to the page as well
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LocationCreate, self).get_context_data(**kwargs)
        # Add in the truck
        context["truck"]=Truck.objects.get(pk=self.kwargs["pk_truck"])
        return context

# renders the delete page for the location
class LocationDelete(DeleteView):
    model = Location

    # returns user to the location list page for their truck upon deletion
    def get_success_url(self, **kwargs):
        return reverse('website:truck-location-list', kwargs={'pk': self.truck_id})

    # deletes the location from the current truck
    def delete(self, request, *args, **kwargs):
        truck = self.get_object().truck
        self.truck_id = truck.id
        return super(LocationDelete, self).delete(request, *args, **kwargs)

#************CRUD for Hours ****************

# renders the hours list page
class HoursListView(ListView):
    model = Hours

    # gets the truck information to be passed to the page as well
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HoursListView, self).get_context_data(**kwargs)
        # Add in the truck
        context["truck"]=Truck.objects.get(pk=self.kwargs["pk"])
        return context

# renders the update page for the operating hours
class HoursItemUpdate(UpdateView):
    model = Hours
    # field selection
    fields =[
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday',]


    template_name_suffix = '_update_form'

    # gets the truck information to be passed to the page as well
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HoursItemUpdate, self).get_context_data(**kwargs)
        # Add in the truck
        context["truck"]=Truck.objects.get(pk=self.kwargs["pk"])
        return context

# renders the create page for operating hours
class HoursCreate(CreateView):
    model = Hours
    # field selection
    fields =[
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday',]

    # saves the new instance to the current truck
    def form_valid(self, form):
        form.instance.truck = Truck.objects.get(pk=self.kwargs['pk_truck'])
        return super(HoursCreate, self).form_valid(form)

    # gets teh truck information to be passed to the page as well
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(HoursCreate, self).get_context_data(**kwargs)
        # Add in the truck
        context["truck"]=Truck.objects.get(pk=self.kwargs["pk_truck"])
        return context

