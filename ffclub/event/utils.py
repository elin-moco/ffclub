# -*- coding: utf-8 -*-
from email.header import Header
import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from ffclub.settings import DEFAULT_FROM_EMAIL, SITE_URL, DEFAULT_REPLY_EMAIL, DEFAULT_NOTIFY_EMAIL
from ffclub.product.tasks import send_mail

log = logging.getLogger('ffclub')


def send_photo_report_mail(from_name, to_name, photo_id):
    subject = Header(u'Firefox 活力軍照片檢舉通知', 'utf-8')
    from_email = DEFAULT_FROM_EMAIL
    log.debug('send to: ' + ''.join(DEFAULT_NOTIFY_EMAIL))
    text_content = render_to_string('event/report_mail.txt',
                                    {'title': subject, 'to_name': to_name, 'from_name': from_name, 'photo_id': photo_id,
                                     'SITE_URL': SITE_URL})
    html_content = render_to_string('event/report_mail.html',
                                    {'title': subject, 'to_name': to_name, 'from_name': from_name, 'photo_id': photo_id,
                                     'SITE_URL': SITE_URL})
    headers = {'Reply-To': DEFAULT_REPLY_EMAIL}
    mail = EmailMultiAlternatives(subject=subject, body=text_content, headers=headers,
                                  from_email=from_email, to=DEFAULT_NOTIFY_EMAIL)
    mail.attach_alternative(html_content, 'text/html')
    send_mail.delay(mail)
