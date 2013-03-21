import logging

from django.shortcuts import render

import commonware
# from commonware import log
from funfactory.log import log_cef
from session_csrf import anonymous_csrf

from ffclub.upload.models import *
from ffclub.upload.forms import *
from forms import *
from models import *


log = commonware.log.getLogger('ffclub')


def wall(request, template=None):
    """Main view."""
    data = {}  # You'd add data here that you're sending to the template.
    log.debug(template)
    return render(request, 'product/wall.html', data)


def order_complete(request, template=None):
    """Main view."""
    data = {}  # You'd add data here that you're sending to the template.
    log.debug(template)
    return render(request, 'product/order_complete.html', data)


def add_product(request, template=None):
    """Main view."""
    data = {'form': ProductForm(), 'upload_form': ImageUploadForm()}  # You'd add data here that you're sending to the template.
    if request.method == 'POST':
        form = ProductForm(request.POST)
        uploadForm = ImageUploadForm(request.POST)
        if form.is_valid():
            form.save()
            log.debug(form)
        else:
            data = {'form': form, 'upload_form': uploadForm}
    log.debug(template)
    return render(request, 'product/add_product.html', data)
