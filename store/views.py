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
    if request.user.is_authenticated:
        customer = request.user.customer
        order ,  created = Order.objects.get_or_create(customer = customer , complete=False)
        items = order.orderitem_set.all()
    else:
        items=[]
    
    message = "This is the cart page"

    context = {'items':items , "order":order}
    return render (request , 'store/cart.html' , context)

def checkout(request):

    message = "This is the checkout page"

    return render (request , 'store/checkout.html' , {"message" : message})

