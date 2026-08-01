from django.urls import path
from . import views

urlpatterns = [
    path("overview/", views.booking_overview, name="booking_overview"),
    path("<int:booking_id>/quotation/", views.quotation, name="quotation"),
    path('create/', views.create_booking, name="create_booking"),
]