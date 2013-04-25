from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline
from .models import *
from ffclub.product.models import Order
from ffclub.upload.admin import ImageUploadInline


class OrderInline(StackedInline):
    model = Order
    extra = 0


class EventAdmin(ModelAdmin):
    search_fields = ['title', 'description', 'location',
                     'orders__usage', 'orders__fullname', 'orders__email',
                     'orders__address', 'orders__occupation', 'orders__feedback']
    list_filter = ['num_of_ppl', 'create_time', 'status', 'orders__create_time', 'orders__status']
    inlines = [OrderInline, ImageUploadInline]


admin.site.register(Event, EventAdmin)
