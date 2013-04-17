# -*- coding: utf-8 -*-
from email.header import Header
import os
import string
import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from ffclub.settings import DEFAULT_FROM_EMAIL, SITE_URL, DEFAULT_REPLY_EMAIL, DEFAULT_NOTIFY_EMAIL
from tasks import send_mail

log = logging.getLogger('ffclub')


def generate_random_string(length, string_set=string.ascii_letters + string.digits + string.punctuation):
    """
    Returns a string with `length` characters chosen from `string_set`
    >>> randomString = generate_random_string(20, string.ascii_letters)
    >>> len(randomString) == 20
    True
    >>> set(randomString) < set(string.ascii_letters)
    True
    """
    return ''.join([string_set[i % len(string_set)]
                    for i in [ord(x) for x in os.urandom(length)]])


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
