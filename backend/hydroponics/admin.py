from django.contrib import admin

from hydroponics.models import HydroponicSystem, Measurement

admin.site.register(HydroponicSystem)
admin.site.register(Measurement)
