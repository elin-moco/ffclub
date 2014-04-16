# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand, BaseCommand
from django.template.loader import render_to_string
from ffclub.settings import MOCO_URL
from ffclub.newsletter.models import *
from ffclub.newsletter.utils import build_meta_params


class Command(BaseCommand):
    help = 'Generate Newslette Static Page'
    option_list = NoArgsCommand.option_list

    def handle(self, *args, **options):

        issue = args[0]
        newsletter = Newsletter.objects.get(issue=issue)
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

        context = {
            'params': params,
            'NEWSLETTER_URL': 'http://'+MOCO_URL+'/newsletter/2014-01/',
            'MOCO_URL': MOCO_URL,
        }

        html_content = render_to_string('newsletter/custom_newsletter_form.html', context)
        text_content = render_to_string('newsletter/newsletter.txt', context)

        with open('%s%s/index.html' % (BEDROCK_NEWSLETTER_PATH, issue), 'w') as newsletter_file:
            newsletter_file.write(html_content.encode('utf-8'))
        with open('%s%s/main.txt' % (BEDROCK_NEWSLETTER_PATH, issue), 'w') as newsletter_file:
            newsletter_file.write(text_content.encode('utf-8'))