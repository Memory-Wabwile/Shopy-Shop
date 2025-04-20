from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Product
from cloudinary.forms import CloudinaryFileField

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username' , 'email' , 'password1' , 'password2']

class ProductForm(forms.ModelForm):
    image = CloudinaryFileField(options = {
        'folder': 'images/',
        'resource_type': 'image',
    })

    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'digital', 'image']


