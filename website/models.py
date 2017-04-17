from __future__ import unicode_literals
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models
import os
import datetime

# Create your models here.

DAYS = (
        (0, 'Sunday'),
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
)


def get_image_path(instance, filename):
    return os.path.join('media', str(instance.id),filename)

# http://stackoverflow.com/questions/8189800/django-store-user-image-in-model

class Truck(models.Model):
    truck_name = models.CharField(max_length=100)
    truck_picture = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    truck_owner = models.ForeignKey(User)
    short_description = models.CharField(max_length=512)
    description = models.TextField()

    def __str__(self):
        return self.truck_name

    def get_absolute_url(self):
        return reverse('website:truck-detail', kwargs={'pk': self.pk})

    def whereami(self):
        print '******'
        lat = "30.615011"
        lon = "-96.342476"
        now = datetime.datetime.now()
        print now
        print self.trucklocation.all()[0].start_time
        print '******'
        for loc in self.trucklocation.all():
            if loc.day == datetime.datetime.today().weekday():
                if loc.start_time < datetime.datetime.now().time() < loc.end_time:
                    lat = loc.latitude
                    lon = loc.longitude
        coordinates = "{lat: %s, lng: %s}" %(lat, lon)
        print coordinates
        return coordinates


class Menu_item(models.Model):
    truck = models.ForeignKey(Truck,related_name='menuitems')
    item_name = models.CharField(max_length=256)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)
    item_description = models.CharField(max_length=256)

    def __str__(self):
        return self.item_name

class Hours(models.Model):
    truck = models.OneToOneField(Truck, related_name='truckhours')
    monday = models.CharField(max_length=256, blank=True, null=True)
    tuesday = models.CharField(max_length=256, blank=True, null=True)
    wednesday = models.CharField(max_length=256, blank=True, null=True)
    thrusday = models.CharField(max_length=256, blank=True, null=True)
    friday = models.CharField(max_length=256, blank=True, null=True)
    saturday = models.CharField(max_length=256, blank=True, null=True)
    sunday = models.CharField(max_length=256, blank=True, null=True)

class Location(models.Model):
    truck = models.ForeignKey(Truck,related_name='trucklocation')
    latitude = models.CharField(max_length=256, blank=True, null=True)
    longitude = models.CharField(max_length=256, blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.IntegerField(choices=DAYS)

    def __str__(self):
        return "%s.%s" %(self.latitude, self.longitude)
