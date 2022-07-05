import json
from .models import *

# cookie cart in charge of cart items for a guest user.. all the views

def cookieCart(request):
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

    return {'cartItems':cartItems , 'order':order , 'items':items}