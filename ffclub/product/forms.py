from django.forms import ModelForm
from ffclub.product.models import Product, Order, OrderDetail


class ProductForm(ModelForm):
    class Meta:
        model = Product


class OrderForm(ModelForm):
    class Meta:
        model = Order


class OrderDetailForm(ModelForm):
    class Meta:
        model = OrderDetail