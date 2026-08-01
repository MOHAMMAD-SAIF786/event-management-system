from django.contrib import admin
from .models import Booking,BookingHall,BookingFurniture,BookingStage,BookingService,BookingRoom
# Register your models here.
admin.site.register(Booking)
admin.site.register(BookingHall)
admin.site.register(BookingFurniture)
admin.site.register(BookingStage)
admin.site.register(BookingService)
admin.site.register(BookingRoom)