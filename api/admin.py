from django.contrib import admin
from api.models import Event, Category, Location, Organizer


admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Organizer)
