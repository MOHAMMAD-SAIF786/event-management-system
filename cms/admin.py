from django.contrib import admin
from catering.models import (
    CateringPackage, 
    CateringFeature, 
    MenuSection, 
    MenuCategory, 
    MenuItem, 
    GuestPricing, 
    BannarFeature
)

class CateringFeatureInline(admin.TabularInline):
    model = CateringFeature
    extra = 1

class BannarFeatureInline(admin.TabularInline):
    model = BannarFeature
    extra = 1

class GuestPricingInline(admin.TabularInline):
    model = GuestPricing
    extra = 1

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1

class MenuCategoryInline(admin.TabularInline):
    model = MenuCategory
    extra = 1

# @admin.register(MenuSection)
# class MenuSectionAdmin(admin.ModelAdmin):
#     list_display = ('title', 'package', 'available_items', 'max_selection', 'order')
#     inlines = [MenuCategoryInline]

# @admin.register(MenuCategory)
# class MenuCategoryAdmin(admin.ModelAdmin):
#     list_display = ('title', 'section', 'order')
#     inlines = [MenuItemInline]

# @admin.register(CateringPackage)
# class CateringPackageAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'badge', 'show_on_home', 'is_active')
#     list_editable = ('price', 'badge', 'show_on_home', 'is_active')
#     prepopulated_fields = {'slug': ('name',)}
#     inlines = [CateringFeatureInline, BannarFeatureInline, GuestPricingInline]