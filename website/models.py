from __future__ import unicode_literals
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.db import models
import os
import datetime

# Create your models here.

#choices for the location model choice field "day"
DAYS = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
)

# gets the location of the image within the media directory. This path is what is stored in the database for the image.
def get_image_path(instance, filename):
    return os.path.join('media', str(instance.id),filename)


# http://stackoverflow.com/questions/8189800/django-store-user-image-in-model

# This is the model that defines the information stored for each truck. Each truck is an instance of this model
class Truck(models.Model):
    truck_name = models.CharField(max_length=100)
    truck_picture = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    truck_owner = models.ForeignKey(User)
    short_description = models.CharField(max_length=512)
    description = models.TextField()

    #returns truck_name instead of truck.object when viewing in admin console
    def __str__(self):
        return self.truck_name
    #gets the url that references a specific instance of a truck so that it can be used in the template
    def get_absolute_url(self):
        return reverse('website:truck-detail', kwargs={'pk': self.pk})
    #returns the current location that is valid based on the time of day
    def whereami(self):
        #now = datetime.datetime.now()
        for loc in self.trucklocation.all():
            #print loc, loc.day, datetime.datetime.today().weekday()
            if loc.day == datetime.datetime.today().weekday():
                if loc.start_time < datetime.datetime.now().time() < loc.end_time:
                    lat = loc.latitude
                    lon = loc.longitude
                    coordinates = "{lat: %s, lng: %s}" %(lat, lon)
                    return coordinates
        return
# This model defines the info stored for each menu item. Each item is an instance of this
class Menu_item(models.Model):
    truck = models.ForeignKey(Truck,related_name='menuitems')
    item_name = models.CharField(max_length=256)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)
    item_description = models.CharField(max_length=256)

    # returns the item_name instead of Menu_item.object when in admin view
    def __str__(self):
        return self.item_name

    #gets the url that references a specific instance of a menu item so that it can be used in the template
    def get_absolute_url(self):
        return reverse_lazy('website:truck-menuitem-list', args=[self.truck.id])

# This model defines the info stored for each set of operating hours. Each instance of this belongs to a truck
class Hours(models.Model):
    truck = models.OneToOneField(Truck, related_name='truckhours') #foreign key to the truck it belongs too. Limits to a single instance per truck
    monday = models.CharField(max_length=256, blank=True, null=True, help_text='256 character limit to express hours as you would like. We recommend something similar to 11am-5pm')
    tuesday = models.CharField(max_length=256, blank=True, null=True, help_text='256 character limit to express hours as you would like. We recommend something similar to 11am-5pm')
    wednesday = models.CharField(max_length=256, blank=True, null=True, help_text='256 character limit to express hours as you would like. We recommend something similar to 11am-5pm')
    thursday = models.CharField(max_length=256, blank=True, null=True, help_text='256 character limit to express hours as you would like. We recommend something similar to 11am-5pm')
    friday = models.CharField(max_length=256, blank=True, null=True, help_text='256 character limit to express hours as you would like. We recommend something similar to 11am-5pm')
    saturday = models.CharField(max_length=256, blank=True, null=True, help_text='256 character limit to express hours as you would like. We recommend something similar to 11am-5pm')
    sunday = models.CharField(max_length=256, blank=True, null=True, help_text='256 character limit to express hours as you would like. We recommend something similar to 11am-5pm')

    #gets the url that references a specific instance of hours so that it can be used in the template
    def get_absolute_url(self):
        return reverse_lazy('website:truck-hours-list', args=[self.truck.id])

# This model defines the info stored for each truck location. Each instance of this belongs to a truck
class Location(models.Model):
    truck = models.ForeignKey(Truck,related_name='trucklocation')
    latitude = models.CharField(max_length=256, blank=True, null=True)
    longitude = models.CharField(max_length=256, blank=True, null=True)
    start_time = models.TimeField(help_text='Please use 24hr format: HH:MM:SS')
    end_time = models.TimeField(help_text='Please use 24hr format: HH:MM:SS')
    # the choices for this are defined globally at the beginning of the file. Gives the user viewable choices for choosing the day the location is valid
    day = models.IntegerField(choices=DAYS)

    # returns the Location coordinates instead of location.object in the admin menu
    def __str__(self):
        return "%s.%s" %(self.latitude, self.longitude)

    # gets the url that references a specefic instance of a location so that it can be used in the template
    def get_absolute_url(self):
        return reverse_lazy('website:truck-location-list', args=[self.truck.id])
