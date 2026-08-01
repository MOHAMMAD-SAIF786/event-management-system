from django.db import models

class Room(models.Model):
    # ROOM_TYPES = (
    #     ('bridal', 'Bridal Suite'),
    #     ('groom', 'Groom Suite'),
    #     ('family', 'Family Room'),
    #     ('ac', 'Guest Room AC'),
    #     ('non_ac', 'Guest Room Non AC'),
    # )

    name = models.CharField(max_length=100)

    # room_type = models.CharField(
    #     max_length=20,
    #     choices=ROOM_TYPES
    # )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    capacity = models.PositiveIntegerField()
    total_rooms = models.PositiveIntegerField(
        default=1
    )

    image = models.ImageField(
        upload_to='rooms/'
    )

    description = models.TextField(blank=True)

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name
    
class RoomFeature(models.Model):

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='features'
    )

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class RoomPage(models.Model):

    hero_title = models.CharField(
        max_length=200,
        default="Room Booking"
    )

    hero_subtitle = models.TextField(
        default="Comfortable & Premium Stay For Your Guests"
    )

    hero_image = models.ImageField(
        upload_to='room_page/'
    )

    def __str__(self):
        return "Room Page Settings"