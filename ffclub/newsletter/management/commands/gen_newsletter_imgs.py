# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand, BaseCommand
from ffclub.newsletter.utils import generate_newsletter_images


class Command(BaseCommand):
    help = 'Generate Newsletter Static Images'
    option_list = NoArgsCommand.option_list

    def handle(self, *args, **options):
        issue = args[0]
        generate_newsletter_images(issue)
