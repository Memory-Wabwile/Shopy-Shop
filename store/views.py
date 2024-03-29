from email import message

from django.http import JsonResponse
from django.shortcuts import render , redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart , cartData , guestOrder
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate , login , logout


# Create your views here.
def registerPage(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            
            #create customer
            Customer.objects.create(user=user, name=username, email=email)
            messages.success(request , 'Account was successfully created for ' + username )
            return redirect('login')


    context = {'form':form}

    return render (request , 'store/register.html' , context)

def loginPage(request):
    if request.method == 'POST':
        username =  request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username , password =password)

        if user is not None:
            login(request,user)
            return redirect('store')
        else:
            messages.info(request , 'username OR password is incorrect')
            
    context = {}

    return render (request , 'store/login.html' , context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def store(request):
    products = Product.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']

    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order ,  created = Order.objects.get_or_create(customer = customer , complete=False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items
       
    #     # for guest user
    # else:
        # items=[]
        # order = {'get_cart_total': 0 , 'get_cart_items':0 , 'shipping':False }
        # cartItems = order['get_cart_items']
   

    context = {'products':products , 'cartItems' : cartItems}
    return render (request , 'store/store.html' ,context)

def cart(request):
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order ,  created = Order.objects.get_or_create(customer = customer , complete=False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items
    # else:
        #copied to utils.py under cookieCart to avoid repetition

    #     try:
    #         cart = json.loads(request.COOKIES['cart'])
    #     except:
    #         cart = {}
    #     print('Cart:' , cart)
    #     items=[]
    #     order = {'get_cart_total': 0 , 'get_cart_items':0 , 'shipping':False }
    #     cartItems = order['get_cart_items']
        
    #     # will show on tha navbar quanityty on cart page for anonymous user
    # for i in cart:
    #     try:
    #         cartItems += cart[i]['quanity']

    #         product = Product.objects.get(id=i)
    #         total = (product.price * cart[i]['quanity'])

    #         order['get_cart_total'] += total
    #         order['get_cart_items'] += cart[i]['quanity']

    #         item = {
    #              'product' : {
    #                  'id' : product.id,
    #                  'name' : product.name,
    #                  'price': product.price,
    #                  'imageURL' : product.imageURL,
    #              },
    #              'quanity' : cart[i]['quanity'],
    #              'get_total' : total,
    #         }
    #         items.append(item)

    #         if product.digital == False :
    #             order['shipping'] = True

    #             # try catch for if a user  adds item to cart and afterwards the item is deleted from the database
    #     except:
    #         pass

        #after cookieCart utils.py
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    message = "This is the cart page"

    context = {'items':items , "order":order , 'cartItems':cartItems}
    return render (request , 'store/cart.html' , context)

def checkout(request):

    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order ,  created = Order.objects.get_or_create(customer = customer , complete=False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items
    # else:
        # items=[]
        # order = {'get_cart_total': 0 , 'get_cart_items':0 , 'shipping':False }
        # cartItems = order['get_cart_items']

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
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
        order , created = Order.objects.get_or_create(customer = customer , complete=False)
       

       
    else:

        customer , order = guestOrder(request,data)
        
    total =float(data['form']['total'])
    order.transaction_id = transaction_id

# to prevent someone from changing the total from the console we have to countercheck the totals to match
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
    return JsonResponse('Payment Complete' , safe=False)
    # create a guest checkout function 

def search(request):
    querry = request.GET['querry']
    products = Product.objects.filter(name__icontains = querry).order_by('-id')

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {'items':items , "order":order , 'cartItems':cartItems ,'products':products }
    return render(request , 'store/search.html', context)

def details(request,id):
    
    productId = ['productId']
  
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
   
    product = Product.objects.get(id=id)
    message = "this is the details page"
    context = {"message":message,
                "product":product,
                'items':items ,
                 "order":order , 
                 'cartItems':cartItems ,}

    return render(request , 'store/details.html', context)