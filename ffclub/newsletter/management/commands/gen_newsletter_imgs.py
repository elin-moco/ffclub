# -*- coding: utf-8 -*-
import csv
from PIL import Image
from django.core.management.base import NoArgsCommand, BaseCommand
from ffclub.newsletter.models import *
import os

ASSETS_PATH = 'static/img/newsletter/'


class Command(BaseCommand):
    help = 'Send Newsletter'
    option_list = NoArgsCommand.option_list

    def handle(self, *args, **options):
        issue = args[0]
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
                self.add_tag(file_path, file_name, tag)

    @staticmethod
    def add_tag(path, name, category):
        background = Image.open(path + '/' + name)
        foreground = Image.open(ASSETS_PATH + 'tag-%s.png' % category)
        background.paste(foreground, (0, 0), foreground)
        background.save(path + '/tagged/' + name)
