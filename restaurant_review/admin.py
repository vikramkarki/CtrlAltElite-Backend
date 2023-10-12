from django.contrib import admin

from .models import Restaurant, Review, Client, Therapist, Appointment

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Review)
admin.site.register(Client)
admin.site.register(Therapist)
admin.site.register(Appointment)
