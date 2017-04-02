from __future__ import unicode_literals
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models
import os

# Create your models here.

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id),filename)

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

class Menu_item(models.Model):
    truck = models.ForeignKey(Truck)
    item_name = models.CharField(max_length=256)
    item_price = models.DecimalField(max_digits=6, decimal_places=2)
    item_description = models.CharField(max_length=256)

class Hours(models.Model):
    truck = models.ForeignKey(Truck)
