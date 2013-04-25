from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from .models import *
from ffclub.upload.admin import ImageUploadInline


class ProductAdmin(ModelAdmin):
    inlines = [ImageUploadInline]
    search_fields = ['title', 'description']
    list_filter = ['quantity', 'create_time', 'status']


class OrderDetailInline(TabularInline):
    model = OrderDetail
    extra = 0


class OrderVerificationInline(TabularInline):
    model = OrderVerification
    extra = 0


class OrderAdmin(ModelAdmin):
    search_fields = ['usage', 'fullname', 'email', 'address', 'occupation', 'feedback', 'details__description']
    list_filter = ['create_time', 'status', 'verification__create_time', 'verification__status']
    inlines = [OrderDetailInline, OrderVerificationInline]

    def __init__(self, model, admin_site):
        super(OrderAdmin, self).__init__(model, admin_site)



admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
