from django.shortcuts import render, redirect
# from .models import Cart
import json
# Create your views here.

def cart(request):
    return render(request, 'cart.html')

def quotation(request):
    return render(request, 'quotation.html')