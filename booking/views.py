from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
import json
from .models import (
    Booking,
    BookingHall,
    BookingRoom,
    BookingFurniture,
    BookingStage,
    BookingService,
    BookingCatering,
    BookingMenuItem,
)
from accounts.models import Customer
from halls.models import (
    Hall,
    FurnitureItem,
    StageDesign,
    Service,
)
from rooms.models import Room
from catering.models import CateringPackage

# Create your views here.
def create_booking(request):

    try:

        data = json.loads(request.body)

        customer_data = data["customer"]

        customer, created = Customer.objects.get_or_create(

            phone=customer_data["phone"],

            defaults={

                "name": customer_data["name"],

                "email": customer_data["email"],
                "address": customer_data.get("address", "")
            }
        )

        booking = Booking.objects.create(

            customer=customer,

            event_date=customer_data["event_date"],

            event_type=customer_data["event_type"]
        )

        total_amount = 0

    # ---------------- Hall ----------------

        hall_data = data.get("hall")

        if hall_data:

            hall = Hall.objects.get(id=hall_data["id"])

            BookingHall.objects.create(

               booking=booking,

               hall=hall,

               price=hall_data["price"]

            )

            total_amount += hall_data["price"]

    # ---------------- Rooms ----------------

        for item in data.get("rooms", []):

            room = Room.objects.get(id=item["id"])

            BookingRoom.objects.create(

                booking=booking,

                room=room,

                quantity=item["quantity"],

                price=item["price"],

                subtotal=item["total"]

            )

            total_amount += item["total"]


    # ---------------- Furniture ----------------

        for item in data["furniture"]:

            furniture = FurnitureItem.objects.get(
                id=item["id"]
            )

            BookingFurniture.objects.create(

                booking=booking,

                furniture=furniture,

                quantity=item["quantity"],

                price=item["price"],

                subtotal=item["total"]

            )

            total_amount += item["total"]

    # ---------------- Stage ----------------

        if data["stage"]:

            stage = StageDesign.objects.get(
                id=data["stage"]["id"]
            )

            BookingStage.objects.create(

                booking=booking,

                stage=stage,

                price=data["stage"]["price"]

            )

            total_amount += data["stage"]["price"]

    # ---------------- Services ----------------

        services = (

            data["entertainment"]

            +

            data["photography"]

            +

            data["guestServices"]

        )

        for item in services:

            service = Service.objects.get(
                id=item["id"]
            )

            BookingService.objects.create(

                booking=booking,

                service=service,

                price=item["price"]

            )

            total_amount += item["price"]
            
    # ---------------- Catering ----------------

        catering_data = data.get("catering")

        if catering_data:

            package = CateringPackage.objects.get(
                id=catering_data["id"]
            )

            booking_catering = BookingCatering.objects.create(

                booking=booking,

                package=package,

                guest_count=catering_data["guestCount"],

                price_per_plate=catering_data["pricePerPlate"],

                total_price=catering_data["total"]
            )

            total_amount += catering_data["total"]

            for menu in catering_data.get("selectedItems", []):

                BookingMenuItem.objects.create(

                    booking_catering=booking_catering,

                    section=menu["section"],

                    item_name=menu["item"]
                )
            
        booking.total_amount = total_amount

        booking.save()

        return JsonResponse({
       "status":"success",
       "booking_id":booking.id,
        })
    except Exception as e:

        return JsonResponse({

            "status": "error",

            "message": str(e)
        }, status=400)
        
def quotation(request, booking_id):

    booking = get_object_or_404(

        Booking.objects.prefetch_related(

            "rooms",

            "furniture",

            "services",

            "catering__menu_items"

        ).select_related(
            "customer",
            "hall_booking__hall",
            "stage__stage",
            "catering__package"
        ),

        id=booking_id

    )

    return render(

        request,

        "quotation.html",

        {

            "booking": booking

        }

    )
    
def booking_overview(request):
    return render(request, "booking_overview.html")
    
