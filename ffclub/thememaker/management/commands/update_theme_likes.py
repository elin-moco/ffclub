# -*- coding: utf-8 -*-
import json
import urllib2
from django.core.management.base import NoArgsCommand, BaseCommand
from django.core.urlresolvers import reverse, resolve
import math
from ffclub.thememaker.models import UserTheme
from ffclub.settings import SITE_URL
from urllib import urlencode


class Command(BaseCommand):
    help = 'Update like count for themes'
    option_list = NoArgsCommand.option_list

    def handle(self, *args, **options):
        self.options = options
        themes = UserTheme.objects.filter(enabled=1)
        urls = []
        for theme in themes:
            urls += [SITE_URL + reverse('thememaker.theme', kwargs={'theme_id': theme.id}), ]

        fbShareData = self.get_fblikes(urls)

        updated = 0
        for url, fbShare in fbShareData.items():
            url = url[len(SITE_URL):]
            args = resolve(url).kwargs
            if 'shares' in fbShare:
                theme = UserTheme.objects.get(pk=int(args['theme_id']))
                if theme.likes != fbShare['shares']:
                    theme.likes = fbShare['shares']
                    theme.save()
                    updated += 1

        print '%d/%d theme updated.' % (updated, len(urls))

    def get_fblikes(self, urls):
        fbShareData = dict()
        chunk_size = 100
        chunks = int(math.floor(len(urls) / chunk_size)) + 1
        for i in range(chunks):
            url_chunk = urls[i * chunk_size: (i + 1) * chunk_size]
            urls = ','.join(url_chunk)
            fbShareData = dict(fbShareData.items() +
                               json.loads(urllib2.urlopen('https://graph.facebook.com/?%s' %
                                                          urlencode({'ids': urls})).read()).items())
        return fbShareData
