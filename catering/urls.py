from django.urls import path
from . import views

urlpatterns = [
    path('', views.catering, name='catering'),
    path('<slug:slug>/',views.package_detail,name='package_detail'),
]