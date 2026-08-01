from django.urls import path
from . import views

urlpatterns = [
    path(
        "<slug:slug>/",
        views.hall_detail,
        name="hall_detail"
    ),
]