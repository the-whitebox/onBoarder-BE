from django.contrib import admin
from business.models import Business, Location, Area, OperatingHours, Shift, Break

# Register your models here.
admin.site.register(Business)
admin.site.register(Location)
admin.site.register(Area)
admin.site.register(OperatingHours)
admin.site.register(Shift)
admin.site.register(Break)
