from django.shortcuts import render
from .models import Room,RoomPage
# Create your views here.
def room(request):
    rooms = Room.objects.filter(
        is_active=True
    )

    room_page = RoomPage.objects.first()

    context = {
        'rooms': rooms,
        'room_page': room_page,
    }
    return render(
        request,
        'room.html',
        context
    )