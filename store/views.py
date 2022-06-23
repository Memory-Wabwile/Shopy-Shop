from email import message
from django.shortcuts import render

# Create your views here.
def store(request):

    message = "Thisis the stores page"

    return render (request , 'store/store.html' , {"message" : message})

def cart(request):

    message = "Thisis the cart page"

    return render (request , 'store/cart.html' , {"message" : message})

def checkout(request):

    message = "This is the checkout page"

    return render (request , 'store/checkout.html' , {"message" : message})

