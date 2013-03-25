# -*- coding: utf-8 -*-
from email.header import Header

from django.contrib import auth
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from ffclub.event.forms import *
from ffclub.upload.forms import *
from forms import *
from models import *
from ffclub.settings import DEFAULT_FROM_EMAIL, SITE_URL
from ffclub.person.models import Person
from utils import *
import logging

log = logging.getLogger('ffclub')


def wall(request):
    if request.user.is_authenticated() and not Person.objects.filter(user=request.user).exists():
        return redirect('user.register')
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
            verification_code = generate_random_string(36, string.ascii_letters + string.digits)
            verification = OrderVerification(order=order, create_user=auth.get_user(request),
                                             code=verification_code)
            verification.save()
            # send verification mail
            subject = Header(u'Firefox活力軍宣傳品申請確認', 'utf-8')
            from_email = DEFAULT_FROM_EMAIL
            to_email = order.email
            log.debug('send to: ' + to_email)
            fullname = order.fullname
            text_content = render_to_string('product/verify_mail.txt',
                                            {'title': subject, 'fullname': fullname, 'code': verification_code,
                                             'SITE_URL': SITE_URL})
            html_content = render_to_string('product/verify_mail.html',
                                            {'title': subject, 'fullname': fullname, 'code': verification_code,
                                             'SITE_URL': SITE_URL})

            mail = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            mail.attach_alternative(html_content, 'text/html')
            mail.send()
            return redirect('product.order.verify')
    else:
        if request.user.is_active:
            profile = request.user.get_profile()
            initialValues = {
                'fullname': profile.fullname,
                'email': request.user.email,
                'address': profile.address,
                'occupation': profile.occupation,
            }
        else:
            initialValues = {}
        eventForm = EventForm()
        orderForm = OrderForm(initial=initialValues)

    orderDetailFormset = OrderDetailFormset()

    products = Product.objects.all()
    for product in products:
        orderDetailForm = OrderDetailForm(initial={'product': product})
        product.orderDetailForm = orderDetailForm
    data = {
        'products': products,
        'event_form': eventForm,
        'order_form': orderForm,
    }
    return render(request, 'product/wall.html', data)


def order_complete(request):
    data = {}
    # You'd add data here that you're sending to the template.
    return render(request, 'product/order_complete.html', data)


def order_verify(request):
    data = {}
    verification_code = request.GET.get('code', None)
    if None != verification_code:
        # verify code
        verifications = OrderVerification.objects.filter(code=verification_code)
        if verifications.exists():
            for v in verifications:
                v.status = 'confirmed'
                v.save()
            return redirect('product.order.complete')
            # You'd add data here that you're sending to the template.
    return render(request, 'product/order_verify.html', data)


def add_product(request):
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
