from email import message
from django.shortcuts import render
from .models import *

# Create your views here.
def store(request):
    products = Product.objects.all()
    # message = "Thisis the stores page"
    context = {'products':products}
    return render (request , 'store/store.html' ,context)

def cart(request):

    message = "Thisis the cart page"

    return render (request , 'store/cart.html' , {"message" : message})

def checkout(request):

    message = "This is the checkout page"

    return render (request , 'store/checkout.html' , {"message" : message})

