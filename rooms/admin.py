from django.contrib import admin
from .models import Room,RoomFeature,RoomPage

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'price',
        'capacity',
        'total_rooms',
        'is_active'
    )

    list_filter = (
        'is_active',
    )

    search_fields = (
        'name',
    )

@admin.register(RoomFeature)
class RoomFeatureAdmin(admin.ModelAdmin):

    list_display = (
        'room',
        'name'
    )

    search_fields = (
        'room__name',
        'name'
    )

@admin.register(RoomPage)
class RoomPageAdmin(admin.ModelAdmin):

    list_display = (
        'hero_title',
    )