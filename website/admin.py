from django.contrib import admin

# Register your models here.

from .models import Truck
from .models import Menu_item
from .models import Hours
from .models import Location
admin.site.register(Truck)
admin.site.register(Menu_item)
admin.site.register(Hours)
admin.site.register(Location)
