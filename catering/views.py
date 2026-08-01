from django.shortcuts import render,get_object_or_404
from .models import CateringPackage

# Create your views here.
def catering(request):
    packages = CateringPackage.objects.filter(
        is_active=True
    )

    context = {
        'packages': packages
    }
    return render(request, 'Caterers/catering.html', context)

def package_detail(request, slug):
    package = get_object_or_404(
        CateringPackage,
        slug=slug
    )
    sections = package.sections.all().order_by(
        'order'
    )

    context = {
        'package': package,
        'sections': sections
    }

    return render(request,'Caterers/package_detail.html', context)