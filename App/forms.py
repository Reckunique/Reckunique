from  django import forms
from App.models import *

class ProductForm(forms.ModelForm):
    class Meta():
        model = Category
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta():
        model = Product
        fields = '__all__'

class CartForm(forms.ModelForm):
    class Meta():
        model = Cart
        fields = ['count']

class CheckoutForm(forms.ModelForm):
    class Meta():
        model=Checkout
        fields='__all__'

class orderform(forms.ModelForm):
    class Meta():
        model=Order
        fields='__all__'
