from email import message
from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json

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
        order = {'get_cart_total': 0 , 'get_cart_items':0}
    message = "This is the cart page"

    context = {'items':items , "order":order}
    return render (request , 'store/cart.html' , context)

def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order ,  created = Order.objects.get_or_create(customer = customer , complete=False)
        items = order.orderitem_set.all()
    else:
        items=[]
        order = {'get_cart_total': 0 , 'get_cart_items':0}
    
    context = {'items':items , "order":order}
    message = "This is the checkout page"

    return render (request , 'store/checkout.html' ,context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:' , action)
    print('productId:' , productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order ,  created = Order.objects.get_or_create(customer = customer , complete=False)

    orderItem ,created = OrderItem.objects.get_or_create() 
    return JsonResponse('Item was added' , safe=False)