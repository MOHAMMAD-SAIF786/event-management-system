from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.utils.timezone import now
from booking.models import Booking
from collections import defaultdict
from accounts.models import Customer
from halls.models import (
    Hall,
    HallFeature,
    HallGallery,
    FurnitureCategory,
    FurnitureItem,
    StageDesign,
    StageCategory,
    ServiceCategory,
    Service
    )
from rooms.models import Room, RoomFeature
from catering.models import (
    BannarFeature,
    CateringPackage,
    CateringFeature,
    GuestPricing,
    MenuCategory,
    MenuItem,
    MenuSection,
)
from .models import GalleryCategory, GalleryItem
from django.utils.text import slugify
from django.http import JsonResponse
from django.views.decorators.http import require_POST



# 1. ADMIN LOGIN VIEW
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('cms:dashboard')

    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')

        user = authenticate(request, username=username_input, password=password_input)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('cms:dashboard')
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, 'cms/login.html')


@login_required(login_url="admin_login")
def dashboard(request):

    total_bookings = Booking.objects.count()

    pending_bookings = Booking.objects.filter(
        status="pending"
    ).count()

    confirmed_bookings = Booking.objects.filter(
        status="confirmed"
    ).count()

    cancelled_bookings = Booking.objects.filter(
        status="cancelled"
    ).count()

    today_bookings = Booking.objects.filter(
        booking_date__date=now().date()
    ).count()

    revenue = Booking.objects.filter(
        status="confirmed"
    ).aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    recent_bookings = Booking.objects.order_by(
        "-booking_date"
    )[:8]

    context = {

        "total_bookings": total_bookings,

        "pending_bookings": pending_bookings,

        "confirmed_bookings": confirmed_bookings,

        "cancelled_bookings": cancelled_bookings,

        "today_bookings": today_bookings,

        "revenue": revenue,

        "recent_bookings": recent_bookings,

    }

    return render(
        request,
        "cms/dashboard.html",
        context
    )


@login_required(login_url="admin_login")
def admin_logout(request):

    logout(request)

    return redirect("admin_login")

# ===========================
# BOOKINGS
# ===========================

def booking_list(request):

    search = request.GET.get("search", "")
    status = request.GET.get("status", "")

    bookings = Booking.objects.all().order_by("-id")

    if search:
        bookings = bookings.filter(customer_name__icontains=search)

    if status:
        bookings = bookings.filter(status=status)

    paginator = Paginator(bookings, 10)

    page = request.GET.get("page")

    bookings = paginator.get_page(page)

    return render(
        request,
        "cms/bookings/list.html",
        {
            "bookings": bookings,
            "search": search,
            "status": status,
        },
    )


def booking_detail(request, id):

    booking = get_object_or_404(
        Booking.objects.select_related(
            "customer",
            "hall_booking__hall",
            "stage__stage",
            "catering__package",
        ).prefetch_related(
            "rooms__room",
            "furniture__furniture",
            "services__service",
            "catering__menu_items",
        ),
        id=id
    )

    menu_sections = defaultdict(list)

    if hasattr(booking, "catering"):

        for item in booking.catering.menu_items.all():

            menu_sections[item.section].append(item)
            
    hall_total = booking.hall_booking.price if hasattr(booking, "hall_booking") else 0

    room_total = sum(room.subtotal for room in booking.rooms.all())

    furniture_total = sum(item.subtotal for item in booking.furniture.all())

    stage_total = booking.stage.price if hasattr(booking, "stage") else 0

    service_total = sum(service.price for service in booking.services.all())

    catering_total = booking.catering.total_price if hasattr(booking, "catering") else 0

    grand_total = (
       hall_total +
       room_total +
       furniture_total +
       stage_total +
       service_total +
       catering_total
)

    return render(
    request,
    "cms/bookings/detail.html",
    {
        "booking": booking,
        "menu_sections": dict(menu_sections),
        "hall_total": hall_total,
        "room_total": room_total,
        "furniture_total": furniture_total,
        "stage_total": stage_total,
        "service_total": service_total,
        "catering_total": catering_total,
        "grand_total": grand_total,
    }
)

@login_required(login_url="admin_login")
def booking_edit(request, id):

    booking = get_object_or_404(
        Booking,
        id=id
    )

    if request.method == "POST":

        booking.customer.name = request.POST.get("customer_name")
        booking.customer.phone = request.POST.get("customer_phone")
        booking.customer.email = request.POST.get("customer_email")

        booking.customer.save()

        booking.event_type = request.POST.get("event_type")
        booking.event_date = request.POST.get("event_date")
        booking.status = request.POST.get("status")

        booking.save()

        messages.success(
            request,
            "Booking Updated Successfully."
        )

        return redirect(
            "booking_detail",
            id=booking.id
        )

    return render(
        request,
        "cms/bookings/edit.html",
        {
            "booking": booking
        }
    )
    
@login_required(login_url="admin_login")
def booking_delete(request, id):

    booking = get_object_or_404(
        Booking,
        id=id
    )

    booking.status = "cancelled"

    booking.save()

    messages.success(
        request,
        "Booking Cancelled Successfully."
    )

    return redirect("cms:booking_list")
    
@login_required(login_url="admin_login")
def customer_list(request):

    search = request.GET.get("search", "")

    customers = Customer.objects.annotate(

        total_bookings=Count("bookings"),

        total_spent=Sum("bookings__total_amount")

    ).order_by("-created_at")

    if search:

        customers = customers.filter(

            name__icontains=search

        ) | Customer.objects.filter(

            phone__icontains=search

        ) | Customer.objects.filter(

            email__icontains=search

        )

    paginator = Paginator(customers, 10)

    page = request.GET.get("page")

    customers = paginator.get_page(page)

    return render(

        request,

        "cms/customers/customer_list.html",

        {

            "customers": customers,

            "search": search,

        }

    )
    
from django.db.models import Sum

@login_required(login_url="admin_login")
def customer_detail(request, id):

    customer = get_object_or_404(Customer, id=id)

    bookings = customer.bookings.all().order_by("-booking_date")

    total_spent = bookings.aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    confirmed = bookings.filter(status="confirmed").count()

    pending = bookings.filter(status="pending").count()

    cancelled = bookings.filter(status="cancelled").count()

    return render(
        request,
        "cms/customers/customer_detail.html",
        {
            "customer": customer,
            "bookings": bookings,
            "total_spent": total_spent,
            "confirmed": confirmed,
            "pending": pending,
            "cancelled": cancelled,
        }
    )
    
@login_required(login_url="admin_login")
def customer_edit(request, id):

    customer = get_object_or_404(
        Customer,
        id=id
    )

    if request.method == "POST":

        customer.name = request.POST.get("name")

        customer.phone = request.POST.get("phone")

        customer.email = request.POST.get("email")

        customer.address = request.POST.get("address")

        customer.save()

        messages.success(
            request,
            "Customer Updated Successfully."
        )

        return redirect(
            "customer_detail",
            id=customer.id
        )

    return render(
        request,
        "cms/customers/customer_edit.html",
        {
            "customer": customer
        }
    )
    
@login_required(login_url="admin_login")
def customer_delete(request, id):

    customer = get_object_or_404(
        Customer,
        id=id
    )

    if customer.bookings.exists():

        messages.error(
            request,
            "Customer cannot be deleted because booking records exist."
        )

        return redirect(
            "customer_detail",
            id=customer.id
        )

    customer.delete()

    messages.success(
        request,
        "Customer deleted successfully."
    )

    return redirect("customer_list")

@login_required(login_url="admin_login")
def hall_list(request):

    halls = Hall.objects.all().order_by("-created_at")

    return render(
        request,
        "cms/halls/hall_list.html",
        {
            "halls": halls
        }
    )
    
@login_required(login_url="admin_login")  
def hall_detail(request, id):

    hall = get_object_or_404(Hall, id=id)

    return render(
        request,
        "cms/halls/hall_detail.html",
        {
            "hall": hall
        }
    )
    
@login_required(login_url="admin_login")
def hall_edit(request, id):

    hall = get_object_or_404(Hall, id=id)

    if request.method == "POST":

        hall.name = request.POST.get("name")
        hall.slug = slugify(request.POST.get("name"))
        hall.description = request.POST.get("description")
        hall.price = request.POST.get("price")
        hall.capacity = request.POST.get("capacity")
        hall.location = request.POST.get("location")
        hall.parking_capacity = request.POST.get("parking_capacity")

        hall.is_ac = "is_ac" in request.POST
        hall.is_wifi = "is_wifi" in request.POST
        hall.is_featured = "is_featured" in request.POST
        hall.is_active = "is_active" in request.POST
        hall.show_badge = "show_badge" in request.POST

        if request.FILES.get("image"):
            hall.image = request.FILES["image"]

        if request.FILES.get("banner_image"):
            hall.banner_image = request.FILES["banner_image"]

        hall.save()

        messages.success(request, "Hall updated successfully.")

        return redirect("cms:cms_hall_detail", id=hall.id)

    return render(
        request,
        "cms/halls/hall_edit.html",
        {
            "hall": hall,
        },
    )
    
@login_required(login_url="admin_login")
def hall_add(request):

    if request.method == "POST":

        slug = slugify(request.POST.get("name"))
        hall = Hall.objects.create(

            name=request.POST.get("name"),
            slug=slug,
            description=request.POST.get("description"),
            price=request.POST.get("price"),
            capacity=request.POST.get("capacity"),
            location=request.POST.get("location"),
            parking_capacity=request.POST.get("parking_capacity"),

            is_ac="is_ac" in request.POST,
            is_wifi="is_wifi" in request.POST,
            is_featured="is_featured" in request.POST,
            is_active="is_active" in request.POST,
            show_badge="show_badge" in request.POST,

            image=request.FILES.get("image"),
            banner_image=request.FILES.get("banner_image"),
        )

        messages.success(request, "Hall created successfully.")

        return redirect("cms:cms_hall_detail", id=hall.id)

    return render(
        request,
        "cms/halls/hall_add.html"
    )

@login_required(login_url="admin_login")
def hall_feature_add(request, hall_id):

    hall = get_object_or_404(Hall, id=hall_id)

    if request.method == "POST":

     HallFeature.objects.create(

       hall=hall,

       title=request.POST.get("title"),

       subtitle=request.POST.get("subtitle"),

       icon="fa-solid fa-check",

       order=HallFeature.objects.filter(hall=hall).count()+1,

    )

    return redirect("hall_edit", id=hall.id)

@login_required(login_url="admin_login")
def hall_feature_edit(request, id):

    feature = get_object_or_404(HallFeature, id=id)

    if request.method == "POST":

        feature.title = request.POST.get("title")
        feature.subtitle = request.POST.get("subtitle")

        feature.save()

        messages.success(request, "Feature Updated Successfully")

        return redirect("hall_edit", id=feature.hall.id)

    return render(
        request,
        "cms/halls/hall_feature_edit.html",
        {
            "feature": feature
        }
    )
    
@login_required(login_url="admin_login")
def hall_feature_delete(request,id):

    feature=get_object_or_404(HallFeature,id=id)

    hall_id=feature.hall.id

    feature.delete()

    messages.success(request,"Feature Deleted")

    return redirect("cms:hall_edit", id=hall_id)

@login_required(login_url="admin_login")
def hall_feature_save(request, hall_id):
    print("POST HIT")
    print(request.POST)
    hall = get_object_or_404(Hall, id=hall_id)

    if request.method == "POST":

        feature_id = request.POST.get("feature_id")

        if feature_id:

            feature = get_object_or_404(HallFeature, id=feature_id)

        else:

            feature = HallFeature(hall=hall)

            feature.icon = "fa-solid fa-check"

            feature.order = HallFeature.objects.filter(hall=hall).count() + 1

        feature.title = request.POST.get("title")

        feature.subtitle = request.POST.get("subtitle")

        feature.save()

        messages.success(request, "Feature Saved Successfully")

    return redirect("cms:hall_edit", id=hall.id)

@login_required(login_url="admin_login")
def hall_gallery_save(request, hall_id):

    hall = get_object_or_404(Hall, id=hall_id)

    if request.method == "POST":

        if request.FILES.get("hall_image"):

            HallGallery.objects.create(

                hall=hall,

                hall_image=request.FILES["hall_image"],

                title=request.POST.get("title"),

                order=HallGallery.objects.filter(hall=hall).count()+1

            )

            messages.success(request, "Gallery Image Added Successfully")

    return redirect("cms:hall_edit", id=hall.id)


@login_required(login_url="admin_login")
def hall_gallery_delete(request, id):

    gallery = get_object_or_404(HallGallery, id=id)

    hall_id = gallery.hall.id

    gallery.delete()

    messages.success(request, "Gallery Image Deleted")

    return redirect("cms:hall_edit", id=hall_id)


@login_required(login_url="admin_login")
def furniture_add(request):

    hall_id = request.GET.get("hall")

    hall = None
    categories = None

    if hall_id:
        hall = get_object_or_404(Hall, id=hall_id)

        categories = FurnitureCategory.objects.filter(
            hall=hall
        ).order_by("order")

    halls = Hall.objects.all()

    return render(
        request,
        "cms/furnitures/furniture_add.html",
        {
            "hall": hall,
            "halls": halls,
            "categories": categories,
            "is_from_hall": bool(hall),
        }
    )
    
@login_required(login_url="admin_login")
def furniture_save(request):

    if request.method == "POST":

        category = get_object_or_404(
            FurnitureCategory,
            id=request.POST.get("category")
        )

        FurnitureItem.objects.create(

            category=category,

            name=request.POST.get("name"),

            price=request.POST.get("price"),

            unit=request.POST.get("unit"),

            default_quantity=request.POST.get("default_quantity"),

            min_quantity=request.POST.get("min_quantity"),

            max_quantity=request.POST.get("max_quantity"),

            is_required="is_required" in request.POST,

            order=FurnitureItem.objects.filter(
                category=category
            ).count()+1

        )

        messages.success(
            request,
            "Furniture Added Successfully"
        )

        return redirect(
            "cms:cms_hall_detail",
            id=category.hall.id
        )
        
@login_required(login_url="admin_login")
def furniture_category_add(request):

    if request.method == "POST":

        hall = get_object_or_404(
            Hall,
            id=request.POST.get("hall")
        )

        FurnitureCategory.objects.create(

            hall=hall,

            name=request.POST.get("category"),

            order=FurnitureCategory.objects.filter(
                hall=hall
            ).count()+1

        )

        messages.success(
            request,
            "Category Created"
        )

        return redirect(
            f"/cms/furniture/add/?hall={hall.id}"
        )
        
@login_required(login_url="admin_login")
def furniture_list(request):

    halls = Hall.objects.prefetch_related(
        "furniture_categories__items"
    ).all()

    return render(
        request,
        "cms/furnitures/furniture_list.html",
        {
            "halls": halls,
        },
    )
    
@login_required(login_url="admin_login")
def furniture_edit(request, id):
    item = get_object_or_404(FurnitureItem, id=id)

    if request.method == "POST":
        item.name = request.POST.get("name")
        item.price = request.POST.get("price")
        item.unit = request.POST.get("unit")
        item.default_quantity = request.POST.get("default_quantity") or 0

        # Empty min/max ko None set karein taaki DB error na aaye
        min_qty = request.POST.get("min_quantity")
        max_qty = request.POST.get("max_quantity")
        item.min_quantity = min_qty if min_qty else None
        item.max_quantity = max_qty if max_qty else None

        item.is_required = "is_required" in request.POST
        item.save()

        messages.success(request, "Furniture Updated Successfully.")

        # HTTP_REFERER: Jis page se request aayi thi (hall_detail ya furniture_list), wahi redirect karega
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)

        return redirect("furniture_list")
@login_required(login_url="admin_login")
def furniture_delete(request, id):

    furniture = get_object_or_404(
        FurnitureItem,
        id=id
    )

    hall = furniture.category.hall

    furniture.delete()

    messages.success(
        request,
        "Furniture Deleted Successfully."
    )

    return redirect("cms:furniture_list")
    
@login_required(login_url="admin_login")
def load_furniture_categories(request, hall_id):

    categories = FurnitureCategory.objects.filter(
        hall_id=hall_id
    ).order_by("order")

    data = []

    for category in categories:

        data.append({
            "id": category.id,
            "name": category.name,
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="admin_login")
def stage_design_list(request):
    # Hall -> StageCategories -> Designs
    halls = Hall.objects.prefetch_related('stage_categories__designs').all()
    return render(request, 'cms/stages/stage_design_list.html', {'halls': halls})

@login_required(login_url="admin_login")
def stage_design_add(request):
    if request.method == "POST":
        category_id = request.POST.get("category_id")
        name = request.POST.get("name")
        price = request.POST.get("price") or 0.00
        image = request.FILES.get("image")

        category = get_object_or_404(StageCategory, id=category_id)

        StageDesign.objects.create(
            category=category,
            name=name,
            price=price,
            image=image
        )

        messages.success(request, "New Stage Design Added Successfully.")

        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect("stage_design_list")

@login_required(login_url="admin_login")
def stage_design_edit(request, id):
    design = get_object_or_404(StageDesign, id=id)

    if request.method == "POST":
        design.name = request.POST.get("name")
        design.price = request.POST.get("price") or 0.00
        
        # Agar nayi image upload hui ho toh update karo
        if request.FILES.get("image"):
            design.image = request.FILES.get("image")

        design.save()
        messages.success(request, "Stage Design Updated Successfully.")

        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect("stage_design_list")


@login_required(login_url="admin_login")
def stage_design_delete(request, id):
    design = get_object_or_404(StageDesign, id=id)
    design.delete()
    messages.success(request, "Stage Design Deleted Successfully.")

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect("stage_design_list")

@login_required(login_url="admin_login")
def stage_category_add(request):
    if request.method == "POST":
        hall_id = request.POST.get("hall_id")
        name = request.POST.get("name")
        description = request.POST.get("description", "")

        hall = get_object_or_404(Hall, id=hall_id)

        StageCategory.objects.create(
            hall=hall,
            name=name,
            description=description
        )

        messages.success(request, f"New Category '{name}' Added Successfully.")

        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect("stage_design_list")


@login_required(login_url="admin_login")
def stage_category_delete(request, id):
    category = get_object_or_404(StageCategory, id=id)
    category.delete()
    messages.success(request, "Category Deleted Successfully.")

    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect("stage_design_list")

# 1. ADD SERVICE CATEGORY
@login_required(login_url="admin_login")
def service_category_add(request):
    if request.method == "POST":
        hall_id = request.POST.get("hall_id")
        name = request.POST.get("name")
        subtitle = request.POST.get("subtitle", "")
        
        hall = get_object_or_404(Hall, id=hall_id)
        ServiceCategory.objects.create(
            hall=hall,
            name=name,
            subtitle=subtitle
        )
        messages.success(request, "New Service Category added successfully.")

        referer = request.META.get('HTTP_REFERER')
        return redirect(referer if referer else "hall_list")

# 2. DELETE SERVICE CATEGORY
@login_required(login_url="admin_login")
def service_category_delete(request, id):
    category = get_object_or_404(ServiceCategory, id=id)
    category.delete()
    messages.success(request, "Service Category deleted successfully.")

    referer = request.META.get('HTTP_REFERER')
    return redirect(referer if referer else "hall_list")

# 3. ADD SERVICE
@login_required(login_url="admin_login")
def service_add(request):
    if request.method == "POST":
        category_id = request.POST.get("category_id")
        name = request.POST.get("name")
        price = request.POST.get("price") or 0.00

        category = get_object_or_404(ServiceCategory, id=category_id)
        Service.objects.create(
            category=category,
            name=name,
            price=price
        )
        messages.success(request, "New Service added successfully.")

        referer = request.META.get('HTTP_REFERER')
        return redirect(referer if referer else "hall_list")

# 4. EDIT SERVICE
@login_required(login_url="admin_login")
def service_edit(request, id):
    service = get_object_or_404(Service, id=id)
    if request.method == "POST":
        service.name = request.POST.get("name")
        service.price = request.POST.get("price") or 0.00
        service.save()
        messages.success(request, "Service updated successfully.")

        referer = request.META.get('HTTP_REFERER')
        return redirect(referer if referer else "hall_list")

# 5. DELETE SERVICE
@login_required(login_url="admin_login")
def service_delete(request, id):
    service = get_object_or_404(Service, id=id)
    service.delete()
    messages.success(request, "Service deleted successfully.")

    referer = request.META.get('HTTP_REFERER')
    return redirect(referer if referer else "hall_list")

@login_required(login_url="admin_login")
@login_required(login_url="admin_login")
def service_list(request):
    halls = Hall.objects.prefetch_related('service_categories__services').all()
    
    return render(request, "cms/services/service_list.html", {"halls": halls})

def room_list(request):
    rooms = Room.objects.prefetch_related('features').all()
    return render(request, 'cms/rooms/room_list.html', {'rooms': rooms})

# 2. Add Room
def room_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        capacity = request.POST.get('capacity')
        total_rooms = request.POST.get('total_rooms', 1)
        description = request.POST.get('description', '')
        image = request.FILES.get('image')
        features_str = request.POST.get('features', '')

        room = Room.objects.create(
            name=name,
            price=price,
            capacity=capacity,
            total_rooms=total_rooms,
            description=description,
            image=image
        )

        # Features add karne ke liye
        if features_str:
            feature_list = [f.strip() for f in features_str.split(',') if f.strip()]
            for feat in feature_list:
                RoomFeature.objects.create(room=room, name=feat)

        return redirect('cms:room_list')

# 3. Edit Room
def room_edit(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        room.name = request.POST.get('name')
        room.price = request.POST.get('price')
        room.capacity = request.POST.get('capacity')
        room.total_rooms = request.POST.get('total_rooms')
        room.description = request.POST.get('description', '')
        
        if request.FILES.get('image'):
            room.image = request.FILES.get('image')
            
        room.save()

        # Features Update
        features_str = request.POST.get('features', '')
        room.features.all().delete()
        if features_str:
            feature_list = [f.strip() for f in features_str.split(',') if f.strip()]
            for feat in feature_list:
                RoomFeature.objects.create(room=room, name=feat)

        return redirect('cms:room_list')

# 4. Delete Room
def room_delete(request, room_id):
    try:
        # room_id se room fetch karein
        room = Room.objects.get(id=room_id)
        room.delete()
        messages.success(request, f'Room #{room_id} deleted successfully!')
    except Room.DoesNotExist:
        # Agar ID 7 database mein nahi hai, tab bhi crash hone se bachega
        messages.error(
            request,
            f'Room with ID #{room_id} does not exist or was already deleted!',
        )
    return redirect('cms:room_list')


def catering_dashboard(request):
    packages = CateringPackage.objects.prefetch_related(
        'features', 'bannar_features', 'guest_pricing', 'sections__categories__items'
    ).all()
    return render(request, 'cms/caterings/catering_list.html', {'packages': packages})

def catering_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description', '')
        badge = request.POST.get('badge', '')
        css_class = request.POST.get('css_class', '')
        show_on_home = request.POST.get('show_on_home') == 'on'
        image = request.FILES.get('image')

        slug = slugify(name)
        orig = slug
        c = 1
        while CateringPackage.objects.filter(slug=slug).exists():
            slug = f"{orig}-{c}"
            c += 1

        pkg = CateringPackage.objects.create(
            name=name, slug=slug, price=price, description=description,
            badge=badge, css_class=css_class, show_on_home=show_on_home, image=image
        )

        # 1. Package Features (Comma separated)
        features_str = request.POST.get('features', '')
        if features_str:
            for f in features_str.split(','):
                if f.strip():
                    CateringFeature.objects.create(package=pkg, name=f.strip())

        # 2. Banner Highlights (Comma separated)
        bannar_str = request.POST.get('bannar_features', '')
        if bannar_str:
            for b in bannar_str.split(','):
                if b.strip():
                    BannarFeature.objects.create(package=pkg, name=b.strip())

        return redirect('catering_list')

def catering_edit(request, package_id):
    pkg = get_object_or_404(CateringPackage, id=package_id)
    if request.method == 'POST':
        pkg.name = request.POST.get('name')
        pkg.price = request.POST.get('price')
        pkg.badge = request.POST.get('badge', '')
        pkg.css_class = request.POST.get('css_class', '')
        pkg.description = request.POST.get('description', '')
        pkg.show_on_home = request.POST.get('show_on_home') == 'on'

        if request.FILES.get('image'):
            pkg.image = request.FILES.get('image')

        pkg.save()

        # Update Features
        pkg.features.all().delete()
        features_str = request.POST.get('features', '')
        if features_str:
            for f in features_str.split(','):
                if f.strip():
                    CateringFeature.objects.create(package=pkg, name=f.strip())

        # Update Banner Features
        pkg.bannar_features.all().delete()
        bannar_str = request.POST.get('bannar_features', '')
        if bannar_str:
            for b in bannar_str.split(','):
                if b.strip():
                    BannarFeature.objects.create(package=pkg, name=b.strip())

        return redirect('catering_list')
    
@require_POST
def catering_delete(request, package_id):
    pkg = get_object_or_404(CateringPackage, id=package_id)
    pkg.delete()
    return redirect('catering_list')

def catering_list(request):
    caterings = Room.objects.prefetch_related('features').all()
    return render(request, 'cms/rooms/catering_list.html', {'caterings': caterings})

@require_POST
def add_menu_item(request, package_id):
    package = get_object_or_404(CateringPackage, id=package_id)
    item_name = request.POST.get('item_name')
    category = request.POST.get('category')
    
    if item_name:
        MenuItem.objects.create(package=package, name=item_name, category=category)
        
    return redirect('package_detail', package_id=package.id)

# Menu item delete karne ke liye
@require_POST
def delete_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    package_id = item.package.id
    item.delete()
    
    return redirect('package_detail', package_id=package_id)

def package_detail_view(request, pk):
    package = get_object_or_404(
        CateringPackage.objects.prefetch_related(
            "guest_pricing",
            "bannar_features",
            "sections__categories__items",
        ),
        pk=pk,
    )

    # --- DELETE REQUESTS (GET Query Parameters) ---
    if "delete_banner_tag" in request.GET:
        BannarFeature.objects.filter(
            id=request.GET.get("delete_banner_tag"), package=package
        ).delete()
        messages.success(request, "Banner tag deleted successfully.")
        return redirect("cms:package_detail", pk=package.pk)

    if "delete_pricing" in request.GET:
        GuestPricing.objects.filter(
            id=request.GET.get("delete_pricing"), package=package
        ).delete()
        messages.success(request, "Pricing slab deleted.")
        return redirect("cms:package_detail", pk=package.pk)

    if "delete_section" in request.GET:
        MenuSection.objects.filter(
            id=request.GET.get("delete_section"), package=package
        ).delete()
        messages.success(request, "Menu section deleted.")
        return redirect("cms:package_detail", pk=package.pk)

    if "delete_category" in request.GET:
        MenuCategory.objects.filter(
            id=request.GET.get("delete_category"), section__package=package
        ).delete()
        messages.success(request, "Category deleted.")
        return redirect("cms:package_detail", pk=package.pk)

    if "delete_item" in request.GET:
        MenuItem.objects.filter(
            id=request.GET.get("delete_item"), section__section__package=package
        ).delete()
        messages.success(request, "Menu item deleted.")
        return redirect("cms:package_detail", pk=package.pk)

    # --- ADD & EDIT REQUESTS (POST) ---
    if request.method == "POST":
        action = request.POST.get("action_type")

        # 1. Update Basic Package Info
        if action == "update_package_info":
            package.name = request.POST.get("name")
            package.price = request.POST.get("price")
            package.badge = request.POST.get("badge")
            package.description = request.POST.get("description")
            if "image" in request.FILES:
                package.image = request.FILES["image"]
            package.save()
            messages.success(request, "Package info updated.")

        # 2. Add / Edit Banner Tag
        elif action == "add_banner_tag":
            tag_name = request.POST.get("tag_name")
            if tag_name:
                BannarFeature.objects.create(package=package, name=tag_name)
                messages.success(request, "Banner tag added.")

        # 3. Add / Edit Guest Pricing
        elif action == "add_guest_pricing":
            GuestPricing.objects.create(
                package=package,
                guest_count=request.POST.get("guest_count"),
                price_per_plate=request.POST.get("price_per_plate"),
            )
            messages.success(request, "Guest pricing added.")

        elif action == "edit_guest_pricing":
            pricing = get_object_or_404(
                GuestPricing, id=request.POST.get("pricing_id"), package=package
            )
            pricing.guest_count = request.POST.get("guest_count")
            pricing.price_per_plate = request.POST.get("price_per_plate")
            pricing.save()
            messages.success(request, "Pricing updated.")

        # 4. Add / Edit Menu Section
        elif action == "add_section":
            MenuSection.objects.create(
                package=package,
                title=request.POST.get("section_title"),
                available_items=request.POST.get("available_items", 0),
                max_selection=request.POST.get("max_selection", 0),
            )
            messages.success(request, "Menu section created.")

        elif action == "edit_section":
            sec = get_object_or_404(
                MenuSection, id=request.POST.get("section_id"), package=package
            )
            sec.title = request.POST.get("section_title")
            sec.available_items = request.POST.get("available_items", 0)
            sec.max_selection = request.POST.get("max_selection", 0)
            sec.save()
            messages.success(request, "Section updated.")

        # 5. Add / Edit Category
        elif action == "add_category":
            sec = get_object_or_404(
                MenuSection, id=request.POST.get("section_id"), package=package
            )
            MenuCategory.objects.create(
                section=sec, title=request.POST.get("category_title")
            )
            messages.success(request, "Category added.")

        elif action == "edit_category":
            cat = get_object_or_404(
                MenuCategory,
                id=request.POST.get("category_id"),
                section__package=package,
            )
            cat.title = request.POST.get("category_title")
            cat.save()
            messages.success(request, "Category updated.")

        # 6. Add Item
        elif action == "add_item":
            cat = get_object_or_404(
                MenuCategory,
                id=request.POST.get("category_id"),
                section__package=package,
            )
            MenuItem.objects.create(
                section=cat, name=request.POST.get("item_name")
            )
            messages.success(request, "Item added.")

        return redirect("cms:package_detail", pk=package.pk)

    return render(
        request, "cms/caterings/package_detail.html", {"package": package}
    )
    
# 1. Main Website Frontend Gallery Page (Aam public ke liye)
def gallery_frontend_view(request):
    categories = GalleryCategory.objects.all()
    items = GalleryItem.objects.select_related("category").all()
    # Path ko 'cms/gallery.html' set karein
    return render(
        request, "gallery.html", {"categories": categories, "items": items}
    )


# 2. CMS Admin Dashboard Gallery Manager View
def cms_gallery_view(request):
    categories = GalleryCategory.objects.all()
    items = GalleryItem.objects.select_related("category").all()

    # 1. Delete Category Logic
    if "delete_category" in request.GET:
        GalleryCategory.objects.filter(
            id=request.GET.get("delete_category")
        ).delete()
        messages.success(request, "Category deleted successfully!")
        return redirect("cms:gallery_dashboard")

    # 2. Delete Image Logic
    if "delete_item" in request.GET:
        GalleryItem.objects.filter(id=request.GET.get("delete_item")).delete()
        messages.success(request, "Image deleted successfully!")
        return redirect("cms:gallery_dashboard")

    # 3. POST Requests (Add Category & Upload Images)
    if request.method == "POST":
        action = request.POST.get("action_type")

        # --- ADD CATEGORY ---
        if action == "add_category":
            cat_name = request.POST.get("name", "").strip()

            if cat_name:
                # Basic Slug Banayein
                base_slug = slugify(cat_name)
                slug = base_slug
                counter = 1

                # Unique Slug Auto-Generate Loop (IntegrityError Se Bachne Ke Liye)
                while GalleryCategory.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1

                # Check if category with exact name exists
                category, created = GalleryCategory.objects.get_or_create(
                    name=cat_name, defaults={"slug": slug}
                )

                if created:
                    messages.success(
                        request, f"Category '{cat_name}' added successfully!"
                    )
                else:
                    messages.warning(
                        request, f"Category '{cat_name}' already exists!"
                    )

        # --- UPLOAD IMAGES ---
        elif action == "upload_images":
            category_id = request.POST.get("category_id")
            images = request.FILES.getlist("images")

            if category_id and images:
                category = get_object_or_404(GalleryCategory, id=category_id)

                for img in images:
                    GalleryItem.objects.create(category=category, image=img)

                messages.success(
                    request,
                    f"{len(images)} Image(s) uploaded successfully to '{category.name}'!",
                )
            else:
                messages.error(
                    request, "Please select a category and at least one image."
                )

        return redirect("cms:gallery_dashboard")

    # Render Template
    return render(
        request, "cms/gallery.html", {"categories": categories, "items": items}
    )
    
def cms_login_view(request):
    # Agar user pehle se logged in hai toh direct dashboard bhej do
    if request.user.is_authenticated:
        return redirect("cms:dashboard")

    if request.method == "POST":
        username_input = request.POST.get("username")
        password_input = request.POST.get("password")

        user = authenticate(
            request, username=username_input, password=password_input
        )

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("cms:dashboard")
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, "cms/login.html")


def cms_logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('cms:login')


# 3. CMS DASHBOARD (Protected)
@login_required(login_url='cms:login')
def cms_dashboard(request):
    return render(request, 'cms/dashboard.html')