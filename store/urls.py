from django.urls import path 
from . import views

urlpatterns = [
    path('' , views.store , name="store"),
    path('cart/' , views.cart , name="cart"),
    path('checkout/' , views.checkout , name="checkout"),
    path('update_item/' , views.updateItem , name="update_item"),
    path('process_order/' , views.processOrder , name="process_order"),
    path('search/', views.search , name="search"),
    path('details/<int:id>', views.details , name="details"),
    path('register/' , views.registerPage, name ="register"),
    path('create_product/', views.create_product, name='create_product'),
    path('login/' , views.loginPage, name ="login"),
    path('logout/' , views.logoutUser, name ="logout"),
    
]
