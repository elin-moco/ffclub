from django.forms import ModelForm
from django.forms.formsets import formset_factory
from ffclub.product.models import Product, Order, OrderDetail


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
        fields = ('quantity',)


OrderDetailFormset = formset_factory(OrderDetailForm)