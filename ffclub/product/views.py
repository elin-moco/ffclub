from django.contrib import auth
from django.shortcuts import render, redirect

import commonware

from ffclub.event.forms import *
from ffclub.upload.forms import *
from forms import *
from models import *


log = commonware.log.getLogger('ffclub')


def wall(request):
    """Main view."""
    if request.method == 'POST':
        eventForm = EventForm(request.POST)
        orderForm = OrderForm(request.POST)
        if eventForm.is_valid() and orderForm.is_valid():
            event = eventForm.save(commit=False)
            order = orderForm.save(commit=False)
            event.create_user = auth.get_user(request)
            order.create_user = auth.get_user(request)
            event.save()
            order.event = event
            order.save()
            return redirect('product.order.complete')
    else:
        eventForm = EventForm()
        orderForm = OrderForm()
    data = {
        'products': Product.objects.all(),
        'event_form': eventForm,
        'order_form': orderForm,
    }
    return render(request, 'product/wall.html', data)


def order_complete(request):
    """Main view."""
    data = {}
    # You'd add data here that you're sending to the template.
    return render(request, 'product/order_complete.html', data)


def add_product(request):
    """Main view."""
    data = {'form': ProductForm(), 'upload_form': ImageUploadForm()}
    if request.method == 'POST':
        form = ProductForm(request.POST)
        uploadForm = ImageUploadForm(request.POST)
        if form.is_valid():
            form.save()
            log.debug(form)
        else:
            data = {'form': form, 'upload_form': uploadForm}
    return render(request, 'product/add_product.html', data)
