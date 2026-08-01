from django.contrib import admin
from .models import HomePage, Feature, ContactInfo
# Register your models here.

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = (
        'hero_title',
    )


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'icon',
    )
    
    search_fields = (
        'title',
    )

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = (
        'address', 
        'phone', 
        'email'
    )
