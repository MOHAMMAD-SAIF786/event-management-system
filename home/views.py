from django.shortcuts import render
from .models import HomePage,Feature, ContactInfo
from rooms.models import Room
from halls.models import Hall
from catering.models import CateringPackage

# Create your views here.
def home(request):
    homepage = HomePage.objects.first()
    features = Feature.objects.all()
    contact = ContactInfo.objects.first()
    rooms = Room.objects.filter(is_active=True)[:3]
    halls = Hall.objects.filter(is_active=True)[:3]
    packages = CateringPackage.objects.filter(
    show_on_home=True,
    is_active=True
)

    context = {
    'homepage': homepage,
    'features': features,
    'contact': contact,
    'rooms': rooms,
    'halls': halls,
    'packages': packages, 
}
    return render(request, 'index.html', context)
