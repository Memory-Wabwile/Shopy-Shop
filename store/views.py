from email import message
from django.shortcuts import render

# Create your views here.
def store(request):

    message = "Thisis the stores page"

    return request (request , 'store/store.html' , {"message" : message})

def cart(request):

    message = "Thisis the cart page"

    return request (request , 'store/cart.html' , {"message" : message})

