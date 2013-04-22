# -*- coding: utf-8 -*-

from email.errors import MessageError
import logging
from email.header import Header

from celery.task import task
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from xlrd import open_workbook
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from ffclub.settings import PRODUCT_INVENTORY_MAPPING, PRODUCT_INVENTORY_QTY_ROW_NAME, \
    PRODUCT_INVENTORY_PATH, PRODUCT_INVENTORY_SHEET_NAME, PRODUCT_INVENTORY_MIN
from ffclub.product.models import Product, Order, OrderDetail
from ffclub.settings import DEFAULT_FROM_EMAIL, SITE_URL, DEFAULT_REPLY_EMAIL, DEFAULT_NOTIFY_EMAIL


log = logging.getLogger('ffclub')


@task()
def send_mail(mail):
    if mail is not None:
        try:
            mail.send()
        except MessageError as e:
            log.debug('Failed to send verification mail: ', e)
        except RuntimeError as e:
            log.debug('Unexpected error when sending verification mail: ', e)


@task()
def sync_inventory():
    book = open_workbook(PRODUCT_INVENTORY_PATH)
    sheet = book.sheet_by_name(PRODUCT_INVENTORY_SHEET_NAME)
    current_qty_row_index = 2
    for row_index in range(sheet.nrows):
        if sheet.cell(row_index, 1).value == PRODUCT_INVENTORY_QTY_ROW_NAME:
            current_qty_row_index = row_index
            print current_qty_row_index
    for col_index in range(sheet.ncols):
        col_name = sheet.cell(0, col_index).value
        if col_name in PRODUCT_INVENTORY_MAPPING.keys():
            product_id = PRODUCT_INVENTORY_MAPPING[col_name]
            #TOTEST: subtrack unprocessed order
            subtracting_quantity = OrderDetail.objects.filter(
                order__status='confirmed', product__id=product_id).aggregate(Sum('quantity'))['quantity__sum']
            quantity = sheet.cell(current_qty_row_index, col_index).value - subtracting_quantity
            try:
                product = Product.objects.get(id=product_id)
                product.quantity = quantity
                product.save()
                log.debug(sheet.cell(0, col_index).value, '(', product_id, '): ', quantity)
            except ObjectDoesNotExist as e:
                log.error('Product with id %d does not exist.' % product_id, e)


@task()
def subtract_product_quantity(order_id):
    order = Order.objects.get(id=order_id)
    orderDetails = order.details.all()
    for orderDetail in orderDetails:
        originalQuantity = orderDetail.product.quantity
        orderDetail.product.quantity -= orderDetail.quantity
        orderDetail.product.save()
        if originalQuantity > PRODUCT_INVENTORY_MIN > orderDetail.product.quantity:
            send_inventory_notification_mail(orderDetail.product)


def send_order_verification_mail(to_name, to_email, verification_code):
    subject = Header(u'Firefox 活力軍宣傳品申請確認', 'utf-8')
    from_email = DEFAULT_FROM_EMAIL
    log.debug('send to: ' + to_email)
    text_content = render_to_string('product/verify_mail.txt',
                                    {'title': subject, 'fullname': to_name, 'code': verification_code,
                                     'SITE_URL': SITE_URL})
    html_content = render_to_string('product/verify_mail.html',
                                    {'title': subject, 'fullname': to_name, 'code': verification_code,
                                     'SITE_URL': SITE_URL})
    headers = {'Reply-To': DEFAULT_REPLY_EMAIL}
    mail = EmailMultiAlternatives(subject=subject, body=text_content, headers=headers,
                                  from_email=from_email, to=[to_email])
    mail.attach_alternative(html_content, 'text/html')
    send_mail.delay(mail)


def send_order_notification_mail(to_name, order_id):
    subject = Header(u'Firefox 活力軍宣傳品新訂單通知', 'utf-8')
    from_email = DEFAULT_FROM_EMAIL
    log.debug('send to: ' + ''.join(DEFAULT_NOTIFY_EMAIL))
    text_content = render_to_string('product/notify_mail.txt',
                                    {'title': subject, 'fullname': to_name, 'order_id': order_id,
                                     'SITE_URL': SITE_URL})
    html_content = render_to_string('product/notify_mail.html',
                                    {'title': subject, 'fullname': to_name, 'order_id': order_id,
                                     'SITE_URL': SITE_URL})
    headers = {'Reply-To': DEFAULT_REPLY_EMAIL}
    mail = EmailMultiAlternatives(subject=subject, body=text_content, headers=headers,
                                  from_email=from_email, to=DEFAULT_NOTIFY_EMAIL)
    mail.attach_alternative(html_content, 'text/html')
    send_mail.delay(mail)


def send_inventory_notification_mail(product):
    subject = Header(u'Firefox 活力軍宣傳品庫存不足通知', 'utf-8')
    from_email = DEFAULT_FROM_EMAIL
    log.debug('send to: ' + ''.join(DEFAULT_NOTIFY_EMAIL))
    text_content = render_to_string('product/inventory_mail.txt',
                                    {'title': subject, 'product': product, 'SITE_URL': SITE_URL})
    html_content = render_to_string('product/inventory_mail.html',
                                    {'title': subject, 'product': product, 'SITE_URL': SITE_URL})
    headers = {'Reply-To': DEFAULT_REPLY_EMAIL}
    mail = EmailMultiAlternatives(subject=subject, body=text_content, headers=headers,
                                  from_email=from_email, to=DEFAULT_NOTIFY_EMAIL)
    mail.attach_alternative(html_content, 'text/html')
    send_mail.delay(mail)
