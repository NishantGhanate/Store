from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models  import User


class ShippingForm(forms.ModelForm):
    class Meta: 
        model = ShippingAddress 
        fields = ['name','phone','address','pincode']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','brand','product_image','sub_category']

class ProductInfoForm(forms.ModelForm):
    class Meta:
        model = ProductInfo
        fields = ['weight','price','quantity','stock']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_no','status']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'