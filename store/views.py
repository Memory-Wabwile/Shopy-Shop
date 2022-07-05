from email import message
from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart

# Create your views here.
def store(request):
    products = Product.objects.all()
    # message = "Thisis the stores page"
    if request.user.is_authenticated:
        customer = request.user.customer
        order ,  created = Order.objects.get_or_create(customer = customer , complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
       
        # for guest user
    else:
        items=[]
        order = {'get_cart_total': 0 , 'get_cart_items':0 , 'shipping':False }
        cartItems = order['get_cart_items']

    context = {'products':products , 'cartItems' : cartItems}
    return render (request , 'store/store.html' ,context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order ,  created = Order.objects.get_or_create(customer = customer , complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        print('Cart:' , cart)
        items=[]
        order = {'get_cart_total': 0 , 'get_cart_items':0 , 'shipping':False }
        cartItems = order['get_cart_items']
        
        # will show on tha navbar quanityty on cart page for anonymous user
    for i in cart:
        try:
            cartItems += cart[i]['quanity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quanity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quanity']

            item = {
                 'product' : {
                     'id' : product.id,
                     'name' : product.name,
                     'price': product.price,
                     'imageURL' : product.imageURL,
                 },
                 'quanity' : cart[i]['quanity'],
                 'get_total' : total,
            }
            items.append(item)

            if product.digital == False :
                order['shipping'] = True

                # try catch for if a user  adds item to cart and afterwards the item is deleted from the database
        except:
            pass

    message = "This is the cart page"

    context = {'items':items , "order":order , 'cartItems':cartItems}
    return render (request , 'store/cart.html' , context)

def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order ,  created = Order.objects.get_or_create(customer = customer , complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order = {'get_cart_total': 0 , 'get_cart_items':0 , 'shipping':False }
        cartItems = order['get_cart_items']
    
    context = {'items':items , "order":order , 'cartItems':cartItems }
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

    orderItem ,created = OrderItem.objects.get_or_create(order = order , product = product) 
    
    if action == 'add':
        orderItem.quanity = (orderItem.quanity + 1)

    elif action == 'remove':
        orderItem.quanity = (orderItem.quanity - 1)

    orderItem.save()

    if orderItem.quanity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added' , safe=False)


# @csrf_exempt
def processOrder(request):

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order ,  created = Order.objects.get_or_create(customer = customer , complete=False)
        total =float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )
    else:
        print("user is not logged in")

    return JsonResponse('Payment Complete' , safe=False)