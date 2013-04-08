# -*- coding: utf-8 -*-

from django.forms import ModelForm, ValidationError
from django.forms.models import BaseInlineFormSet
from ffclub.product.models import Product, Order, OrderDetail
import logging

log = logging.getLogger('ffclub')


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
        log.error('clean!!!!!!!!!!')
        hasOrderDetail = False
        for orderDetailForm in self.forms:
            if orderDetailForm.cleaned_data['quantity'] > 0:
                hasOrderDetail = True
        log.error('hasOrderDetail: %d' % hasOrderDetail)
        if not hasOrderDetail:
            log.error('invalid!!!!!!!!!!')
            raise ValidationError('請至少選擇一項宣傳品')
