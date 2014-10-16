# -*- coding: utf-8 -*-
from email.header import Header
import commonware.log
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from ffclub.settings import DEFAULT_FROM_EMAIL, SITE_URL, DEFAULT_REPLY_EMAIL, DEFAULT_NOTIFY_EMAIL, BEDROCK_PATH, FFCLUB_URL
from ffclub.product.tasks import send_mail
from ffclub.person.models import Person
from ffclub.event.models import Vote
from django.db.models import Count
from random import choice
import string
import bisect
import random
from collections import Sequence
import qrcode
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import re

log = commonware.log.getLogger('ffclub')


def prefetch_votes(uploads, contentType, currentUser):
    ids = []
    for upload in uploads:
        if upload.id not in ids:
            ids += (upload.id,)
    voted = Vote.objects.filter(entity_id__in=ids, content_type=contentType, voter=currentUser).values_list('entity_id', flat=True) \
        if currentUser else []

    votes = Vote.objects.filter(entity_id__in=ids, content_type=contentType).values('entity_id').annotate(vote_count=Count('entity_id'))
    for upload in uploads:
        upload.vote_count = 0
        upload.voted = False
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


def generate_claim_code(length=6):
    return ''.join(choice(string.ascii_uppercase + string.digits) for x in range(length))


def weighted_sample(population, weights, amount=1):
    return random.sample(WeightedSequence(population, weights), amount)


class WeightedSequence(Sequence):
    def __init__(self, population, weights):
        assert len(population) == len(weights) > 0
        self.population = population
        self.cumweights = []
        cumsum = 0
        for w in weights:
            cumsum += w
            self.cumweights.append(cumsum)

    def __len__(self):
        return self.cumweights[-1]

    def __getitem__(self, i):
        if not 0 <= i < len(self):
            raise IndexError(i)
        return self.population[bisect.bisect(self.cumweights, i)]


def make_white_transparent(img):
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    return img


def get_font(text, size):
    if isinstance(text, unicode):
        font = ImageFont.truetype('media/fonts/wt014.ttf', size)
    else:
        font = ImageFont.truetype('media/fonts/OpenSans-Bold-webfont.ttf', size)
    return font


def generate_10years_ticket(session, code):
    validation_url = 'https://%s/campaign/10years/firefox-family/validate?code=%s' % (FFCLUB_URL, code)
    ticket_info = u'場次：%s  序號：%s' % (session, code)
    rules1 = u'請將此票券列印下來，或者儲存在你的手機、'
    rules2 = u'平板上，活動當天於入口櫃台掃描條碼，即可'
    rules3 = u'完成報到程序優先入場，並領取早鳥抽獎券。'
    rules4 = u'* 請注意：一組條碼只能使用一次。'
    filename = '%s-%s.png' % (re.sub('[:/\s]', '', session), code)
    qr = qrcode.make(validation_url)
    qr = make_white_transparent(qr)
    qr.thumbnail((200, 200), Image.NEAREST)

    bg = Image.open(BEDROCK_PATH + 'media/img/mocotw/10years/fx-family/ticket/ticket-print.png')
    bg.paste(qr, (380, 56), qr)

    draw = ImageDraw.Draw(bg)
    draw.text((114, 223), ticket_info, (0, 0, 0), font=get_font(ticket_info, 16))
    rules_font = get_font(rules1, 13)
    draw.text((116, 112), rules1, (0, 0, 0), font=rules_font)
    draw.text((116, 132), rules2, (0, 0, 0), font=rules_font)
    draw.text((116, 152), rules3, (0, 0, 0), font=rules_font)
    draw.text((116, 192), rules4, (0, 0, 0), font=rules_font)

    bg.save(BEDROCK_PATH + 'media/img/mocotw/10years/fx-day/tickets/' + filename)
