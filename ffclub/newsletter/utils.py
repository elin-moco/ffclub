# -*- coding: utf-8 -*-
from email.errors import MessageError
from email.header import Header
from time import sleep
from BeautifulSoup import BeautifulSoup
import commonware.log
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import *
import os
from ffclub.settings import NEWSLETTER_ASSETS_URL, BEDROCK_NEWSLETTER_PATH, MOCO_URL, MYFF_URL, FFCLUB_URL, TECH_URL, BEDROCK_GA_ACCOUNT_CODE, NEWSLETTER_PRESEND_LIST
from PIL import Image
import premailer


log = commonware.log.getLogger('ffclub')


def build_meta_params(all_metadata=None, admin=False):
    params = {}

    if all_metadata:
        tags = {}
        for meta in all_metadata:
            if isinstance(meta, MetaString) and meta.name.endswith('-tag'):
                key = meta.name[:-4]
                if key not in tags:
                    tags[key] = {}
                tags[key][meta.index] = meta.value

        for meta in all_metadata:
            val = meta.value
            if isinstance(meta, MetaDatetime):
                val = val.strftime('%Y/%m/%d')
            elif isinstance(meta, MetaFile):
                key = meta.name[:meta.name.rfind('-')]
                val = NEWSLETTER_ASSETS_URL + ('' if admin or not (key in tags or meta.name == 'video-thumb') else 'tagged/') + os.path.basename(val.file.name)
            if meta.index == 0:
                params[meta.name] = val
            else:
                if meta.name not in params:
                    params[meta.name] = {}
                params[meta.name][meta.index] = val

    if 'article-thumb' not in params:
        params['article-thumb'] = {}
    if 'article-link' not in params:
        params['article-link'] = {}
    if 'article-tag' not in params:
        params['article-tag'] = {}
    if 'article-title' not in params:
        params['article-title'] = {}
    if 'article-desc' not in params:
        params['article-desc'] = {}
    if 'video-thumb' not in params:
        params['video-thumb'] = {}
    if 'video-link' not in params:
        params['video-link'] = {}
    if 'video-tag' not in params:
        params['video-tag'] = {}
    if 'video-title' not in params:
        params['video-title'] = {}
    if 'video-desc' not in params:
        params['video-desc'] = {}
    if 'video-length' not in params:
        params['video-length'] = {}
    if 'quiz-answer' not in params:
        params['quiz-answer'] = {}

    return params


def newsletter_subscribe(email):
    if not email:
        return False
    existingEmails = Subscription.objects.filter(email=email)
    if not existingEmails.exists():
        subscription = Subscription(email=email.lower())
        subscription.save()
        log.info(email + ' subscribed!')
        return True
    else:
        log.warning(email + ' already exists!')
        for existingEmail in existingEmails:
            if 0 == existingEmail.status:
                existingEmail.status = 1
                existingEmail.save()
    return False


def newsletter_unsubscribe(emailAddress):
    emails = Subscription.objects.filter(email=emailAddress)
    if emails.exists():
        for email in emails:
            email.status = 0
            email.save()
            log.info(emailAddress + ' unsubscribed!')
        return True
    else:
        log.warning(emailAddress + ' does not exists!')
        return False


def read_newsletter_context(issue, is_web=False):
    newsletter = Newsletter.objects.get(issue=issue)
    ymd = issue[2:4] + issue[5:7] + (issue[8:10] if len(issue) > 7 else '')

    params = {
        'title': newsletter.title,
        'issue': newsletter.issue.strftime('%Y年%m月%d號').decode('utf-8'),
        'volume': newsletter.volume,
    }
    all_metadata = list(MetaString.objects.filter(issue=newsletter)) + \
                   list(MetaDatetime.objects.filter(issue=newsletter)) + \
                   list(MetaNumber.objects.filter(issue=newsletter)) + \
                   list(MetaFile.objects.filter(issue=newsletter))
    params = dict(params.items() + build_meta_params(all_metadata).items())

    if not is_web:
        params['tracking_code'] = '?utm_source=epaper&utm_medium=email&utm_campaign=epaper%s&utm_content=mozilla' % ymd

    return {
        'params': params,
        'BEDROCK_GA_ACCOUNT_CODE': BEDROCK_GA_ACCOUNT_CODE,
        'NEWSLETTER_URL': 'http://%s/newsletter/%s/' % (MOCO_URL, issue),
        'MOCO_URL': MOCO_URL,
        'MYFF_URL': MYFF_URL,
        'FFCLUB_URL': FFCLUB_URL,
        'TECH_URL': TECH_URL,
        'request': is_web
    }


def generate_newsletter(issue, is_web=False):
    context = read_newsletter_context(issue, is_web)
    html_content = render_to_string('newsletter/custom_newsletter_form.html', context)
    text_content = render_to_string('newsletter/newsletter.txt', context)

    issue_path = '%s%s/' % (BEDROCK_NEWSLETTER_PATH, issue)
    if not os.path.exists(issue_path):
        os.makedirs(issue_path)
    with open('%sindex.html' % issue_path, 'w') as newsletter_file:
        newsletter_file.write(html_content.encode('utf-8'))
    with open('%smail.txt' % issue_path, 'w') as newsletter_file:
        newsletter_file.write(text_content.encode('utf-8'))


def generate_newsletter_images(issue):
    newsletter = Newsletter.objects.get(issue=issue)
    all_meta_string = MetaString.objects.filter(issue=newsletter)

    tags = {}
    for meta_string in all_meta_string:
        if meta_string.name.endswith('-tag'):
            key = meta_string.name[:-4]
            if key not in tags:
                tags[key] = {}
            tags[key][meta_string.index] = meta_string.value

    all_meta_file = MetaFile.objects.filter(issue=newsletter)
    for meta_file in all_meta_file:
        key = meta_file.name[:meta_file.name.rfind('-')]
        if key in tags.keys():
            tag = tags[key][meta_file.index]
            file_path = os.path.dirname(meta_file.value.path)
            file_name = os.path.basename(meta_file.value.path)
            add_tag(file_path, file_name, tag)
        elif meta_file.name == 'video-thumb':
            file_path = os.path.dirname(meta_file.value.path)
            file_name = os.path.basename(meta_file.value.path)
            add_play_icon(file_path, file_name)


def add_tag(path, name, category):
    background = Image.open(path + '/' + name)
    foreground = Image.open('static/img/newsletter/tag-%s.png' % category)
    background.paste(foreground, (0, 0), foreground)
    background.save(path + '/tagged/' + name)


def add_play_icon(path, name):
    background = Image.open(path + '/' + name)
    foreground = Image.open('static/img/newsletter/play-btn.png')
    background.paste(foreground, (70, 37), foreground)
    background.save(path + '/tagged/' + name)


def send_mail(subject, headers, from_email, to_mail, text_content, mail_content, issue_number):
    mail = EmailMultiAlternatives(subject=subject, body=text_content, headers=headers,
                                  from_email=from_email, to=to_mail)
    mail.attach_alternative(mail_content, 'text/html')

    try:
        mail.send()
        print('Sent newsletter to %s.' % to_mail)
    except MessageError as e:
        print('Failed to send to %s.' % to_mail, e)
    except RuntimeError as e:
        print('Unexpected error when sending to %s.' % to_mail, e)


def named(email, name):
    if name:
        return '%s <%s>' % (name, email)
    return email


def send_newsletter(issue_number, to_mail):
    context = read_newsletter_context(issue_number)
    from_email = '"Mozilla Taiwan" <no-reply@mozilla.com.tw>'
    text_content = render_to_string('newsletter/newsletter.txt', context)
    html_content = render_to_string('newsletter/custom_newsletter_form.html', context)
    mail_content = premailer.transform(html_content)
    soup = BeautifulSoup(html_content)
    subject = Header((u'[測試] ' if to_mail else '') + soup.title.string, 'utf-8')
    headers = {}
    if not to_mail:
        with open('subscriptions.txt') as file:
            subscriptions = file.readlines()
            for subscription in subscriptions:
                send_mail(subject, headers, from_email, (subscription.rstrip(), ),
                               text_content, mail_content, issue_number)
                sleep(10)
    elif to_mail == 'presend':
        for mail_address in NEWSLETTER_PRESEND_LIST:
            send_mail(subject, headers, from_email, (mail_address, ), text_content, mail_content, issue_number)
            sleep(10)
    else:
        send_mail(subject, headers, from_email, (to_mail, ), text_content, mail_content, issue_number)
