# -*- coding: utf-8 -*-
from email.header import Header
import commonware.log
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from ffclub.settings import DEFAULT_FROM_EMAIL, SITE_URL, DEFAULT_REPLY_EMAIL, DEFAULT_NOTIFY_EMAIL
from ffclub.product.tasks import send_mail
from ffclub.person.models import Person
from ffclub.event.models import Vote
from django.db.models import Count

log = commonware.log.getLogger('ffclub')


def prefetch_votes(uploads, currentUser):
    ids = []
    for upload in uploads:
        if upload.id not in ids:
            ids += (upload.id,)
    voted = Vote.objects.filter(entity_id__in=ids, voter=currentUser).values_list('entity_id', flat=True) \
        if currentUser else []
    print voted
    votes = Vote.objects.filter(entity_id__in=ids).values('entity_id').annotate(vote_count=Count('entity_id'))
    for upload in uploads:
        upload.vote_count = 0
        for vote in votes:
            if upload.id == vote['entity_id']:
                upload.vote_count = vote['vote_count']
            upload.voted = True if upload.id in voted else False
    return uploads


def prefetch_profile_name(uploads):
    uids = []
    for upload in uploads:
        if upload.create_user.id not in uids:
            uids += (upload.create_user.id,)
    people = Person.objects.filter(user_id__in=uids)
    for upload in uploads:
        for person in people:
            if upload.create_user.id == person.user_id:
                upload.create_username = person.nickname
    return uploads


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
