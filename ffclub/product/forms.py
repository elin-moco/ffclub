# -*- coding: utf-8 -*-

import commonware.log

from django.forms import ModelForm, ValidationError
from django.forms.models import BaseInlineFormSet

from ffclub.product.models import Product, Order, OrderDetail


log = commonware.log.getLogger('ffclub')


class ProductForm(ModelForm):
    class Meta:
        model = Product


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ('usage', 'fullname', 'email', 'address', 'occupation', 'feedback')


class OrderDetailForm(ModelForm):
    class Meta:
        model = OrderDetail
        fields = ('quantity', 'product')


class BaseOrderDetailFormSet(BaseInlineFormSet):
    def clean(self):
        hasOrderDetail = False
        for orderDetailForm in self.forms:
            if orderDetailForm.cleaned_data['quantity'] > 0:
                hasOrderDetail = True
        if not hasOrderDetail:
            raise ValidationError('請至少選擇一項宣傳品')
