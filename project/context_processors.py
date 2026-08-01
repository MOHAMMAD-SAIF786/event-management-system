from halls.models import Hall

def hall_menu(request):
    return {
        "hall_menu": Hall.objects.filter(is_active=True).order_by("name")
    }