from django.shortcuts import render, get_object_or_404
from .models import Hall

# Create your views here.
def hall_detail(request, slug):
    hall = get_object_or_404(
        Hall,
        slug=slug,
        is_active=True
    )
    halls = Hall.objects.filter(
        is_active=True
    )

    return render(
        request,
        "halls/hall_detail.html",
        {
            "hall":hall,
            "halls":halls
        }
    )
