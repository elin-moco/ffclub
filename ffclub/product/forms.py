from django.forms import ModelForm
from ffclub.product.models import Product, Order, OrderDetail
from django import forms


class ProductForm(ModelForm):
    class Meta:
        model = Product


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('usage', 'fullname', 'email', 'address', 'occupation')


class OrderDetailForm(ModelForm):

    class Meta:
        model = OrderDetail
        fields = ('quantity', 'product')
